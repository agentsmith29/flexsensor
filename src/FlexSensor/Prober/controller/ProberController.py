import logging

from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
from Prober.controller.OpticalInterface import OpticalInterface
import Prober
from Prober.model.ProberModel import ProberModel
from constants.FlexsensorConstants import Probe
from generics.generics import pch


class ProberController:
    def __init__(self, model: ProberModel, vaut_config: VAutomatorConfig, *args, **kwargs):

        self.vaut_config = vaut_config
        self.model = model

        self.model.wafer_map = self.vaut_config.wafer_config.wafermap_file

        self.logger = logging.getLogger("Prober")
        self.signals = Prober.Signals()
        self.msg_server = Prober.MessageServerInterface()

        # Optical Interface Control hexapods and piezos
        self.opt_if = OpticalInterface(self.signals, self.msg_server)
        self.logger.info("Prober initialized")

        self.model.version = self.report_kernel_version()
        self.get_die_as_col_row()
        self.read_chuck_position()
        self.model.connected = True

    # ==================================================================================================================
    # Velox API Calls.
    # Some Wrappers to the official Velox API calls
    # ==================================================================================================================
    def set_chuck_home(self, mode: str = '0', unit: str = 'Y', x_value: float = 0, y_value: float = 0):
        """ Velox API Call. Sets wafer and die home position, which can be used later as coordinate system
        for movements.
        Keyword arguments:
            mode: str -- '0' use the current position or the given value otherwise. (default "0")
            unit: str -- Sets the unit (Y: 'Microns' or I 'Mils'). Required if mode is not set to default (Y).
                (default 'Microns')
            x_value: float -- Required if mode is not set to V. (default 0)
            y_value: float -- Required if mode is not set to V. (default 0)
        Command Timeout: 5000
        """
        self.logger.info(f"[Prober Task] - Set Chuck home. Issuing command 'SetChuckHome({mode})'")
        self.signals.log_info.emit("Prober Report", f"Set Chuck Home.", None)
        Prober.SetChuckHome(str(mode), str(unit), x_value, y_value)

    def set_map_home(self, col=0, row=0):
        """ Velox API Call. If the command has no parameters it sets the current position as home position
            both for the wafer map and for the chuck. Otherwise, it changes the wafer map
            home position using the given die coordinates.
            Keyword arguments:
                col: int -- Column (optional). (default 0)
                row: int -- Row (optional). (default 0)
            Command Timeout: 10000
        """
        self.logger.info(f"[Prober Task] - Set Map home to col {col} and row {row}. "
                         f"Issuing command 'SetMapHome({col}, {row})'")
        self.signals.log_info.emit("Prober Report", f"Map Home set to {col}, {row}.", None)
        Prober.SetMapHome(col, row)

    def read_chuck_position(self, unit: str = "Microns", pos_ref: str = "Home", comp: str = "Default") -> (float, float, float):
        """ Velox API Call. Returns the current chuck stage position in X, Y and Z.
        Args:
            unit:str = "Microns"
            pos_ref:str = "Home"
            comp:str = "Default"
        Returns:
            X:float
            Y:float
            Z:float
        Command Timeout: 5000
        """
        self.model._chuck_x, self.model._chuck_y, self.model._chuck_z = Prober.ReadChuckPosition(Unit=unit, PosRef=pos_ref)
        self.logger.info(f"[Prober Report] - "
                         f"Current Chuck position X:{self.model._chuck_x} Y:{ self.model._chuck_y} Z:{self.model._chuck_z}")
        self.signals.log_info.emit("Prober Report",
                                   f"Current Chuck position "
                                   f"X:{self.model._chuck_x} "
                                   f"Y:{ self.model._chuck_y} "
                                   f"Z:{self.model._chuck_z}", None)
        return float(self.model._chuck_x), float(self.model._chuck_y), float(self.model._chuck_z)

    def check_contact_height_set(self) -> (float, float, float, float, float):
        """ Velox API Call. Returns the current settings used for the chuck Z movement. `Contact` is the
            contact-height from zero in default compensation. The other heights are relative
            to this. If no contact is set, an error will be raised.
            API Status: published
            Args:
                Unit:str = "Microns"
            Returns:
                Contact:Decimal
                Overtravel:Decimal
                AlignDist:Decimal
                SepDist:Decimal
                SearchGap:Decimal
            Command Timeout: 5000
        """
        self.logger.debug("[Prober Task] - Check if contact height is set. Issuing command 'ReadChuckHeights'")
        self.signals.log_debug.emit("Prober Task", "Check if contact height is set. Issuing command 'ReadChuckHeights'",
                                    None)
        contact, overtravel, align_dist, sep_dis, search_gap = Prober.ReadChuckHeights()

        if contact == -1:
            self.logger.error("[Prober Task] - Contact height not set, please set it before running this script. "
                              "Script will be stopped.")
            raise Exception("Contact height not set, please set it before running this script. Script will be stopped.")

        self.logger.debug(f"[Prober Task] - Contact height set to {contact}")
        self.signals.log_debug.emit("Prober Task", f"Contact height set to {contact}", None)

        return float(contact), float(overtravel), float(align_dist), float(sep_dis), float(search_gap)

    def move_chuck(self, x_value: float = 0, y_value: float = 0,
                   pos_ref: str = "H", unit: str = "Y", velocity: float = 100, comp: str = "D"):
        """ Velox API Call. Moves the chuck stage to the specified X,Y position. If chuck Z is in contact
           height or higher, Interlock and Auto Z flags will be analyzed and stage will
           behave correspondingly - can move to separation first or return an error:
           Keyword arguments:
               x_value:float -- X Value (optional). (default 0)
               y_value:float -- Y Value (optional). (default 0)
               pos_ref:str -- "H: Home", "Z: Zero", "C: Center", "R: Current Position". (default "H: Home")
               unit:str -- "Y: Microns", "I: Mils", "X: Index", "J: Jog". (default "M: Microns")
               velocity:float -- Velocity in percent. (default 100)
               comp:str
                    "D: Default": Use the default compensation. Uses "Technology" by default.
                    "T: Technology": Use Prober, offset and Technology compensation. (default)
                    "O: Offset": Use Prober and Offset compensation.
                    "P: Prober" Use only Prober compensation.
                    "N: None": Does not use compensation.
                (default "D: Default")
           Command Timeout: 30000
           """
        self.logger.debug(f"[Prober Task] - Move Chuck to x: {x_value} y: {y_value}. "
                          f"Issuing command 'MoveChuck({x_value}, {y_value}, {pos_ref}, {unit}, {velocity}, {comp})'")
        self.signals.log_debug.emit("Prober Task", f"Move Chuck to x: {x_value} y: {y_value}", None)
        Prober.MoveChuck(x_value, y_value, pos_ref, unit, velocity, comp)

    def snap_image(self, mount_pos: str = "eVue2", full_path: str = "./Image.bmp", snap_shot_mode: int = 2):
        """
            Velox API Call. Saves the currently displayed image to the specified file. The image is stored
            in the requested file format (bmp, jpg or png). By default. it will save the raw
            camera image and an image with the overlays that are currently visible on the
            camera view. Using a parameter, one can decide to only save either raw image,
            overlay image or both. By Specifying 'ALL' as the mount position, the captured
            screenshot will consist of the currently selected camera layout without
            providing the raw image. If MountPos and FullPath are empty then the current
            camera view with overlays is copied to the clipboard.
            API Status: published
            Args:
                mount_pos:str -- Mount position of camera from which the image will be taken:
                    'Scope', 'eVue1', 'eVue2', 'eVue3', 'Chuck', 'Platen', 'ContactView', or 'All'.
                    (default "eVue2")

                    (If you use ‘Scope’ on a system with eVue, the image will be from eVue2).
                    If set to ‘All’ the currently visible camera layout will be captured in the screenshot
                    "eVue2".
                full_path:str -- Path where the image will be stored. (default: "./Image.bmp")
                snap_shot_mode:int -- Type of snapshot (default 2)
                    0 – Raw Image from camera
                    1 – Screenshot of camera window including overlays;
                    2 – Both images
            Example:SnapImage Scope C:/Temp/Image.bmp
            """
        self.logger.debug(f"[Prober Task] - Save scope image {mount_pos} to {full_path} (mode: {snap_shot_mode}). "
                          f"Issuing command 'SnapImage({mount_pos}, {full_path}, {snap_shot_mode})'")
        self.signals.log_debug.emit("Prober Task",
                                    f"Save scope image {mount_pos} to {full_path} (mode: {snap_shot_mode}).", None)
        Prober.SnapImage(mount_pos, full_path, snap_shot_mode)

    def report_kernel_version(self):
        v = Prober.ReportKernelVersion()
        self.model.kernel_version = str(v.Version) + "." + str(v.Description)
        return str(v.Version) + "." + str(v.Description)

    def get_die_as_col_row(self):
        # Read the die data: die number, col, row
        self.model.die, self.model.die_col, self.model.die_row, bin, res = Prober.GetDieDataAsColRow()
        self.logger.info(f"[Prober Report] - Current die number: {self.model.die} "
                         f"(col: {self.model.die_col}, row: {self.model.die_row})")
        self.signals.log_info.emit("Prober Report", f"Current die number: {self.model.die} "
                                                    f"(col: {self.model.die_col}, row: {self.model.die_row})", None)
        return self.model.die, self.model.die_col, self.model.die_row
    # ==================================================================================================================
    #
    # ==================================================================================================================
    def move_to_die(self, die_num=0) -> (float, float, float):
        '''
        Move to the specified die and sets the home position accordingly
        '''

        # TODO: check if die is in the correct position and check if height is correct
        self.logger.debug(f"[Prober Task] - {pch('*', 20)} Moving to die {die_num} {pch('*', 20)}")
        self.signals.log_debug.emit("Prober Task", f"*** Moving to die {die_num} ***", None)

        # We need to make sure that our fiber height is correct
        # TODO: Check fiber height - this is important! IMPLEMENT HERE
        # ...
        # ...
        # raise NotImplementedError("Check fiber hight not implemented yet")

        # Move to die
        # Disable the flight height control
        self.opt_if.enable_flight_height_control(enable_in=False, enable_out=False)

        # FindOpticalProbeHeight(0, 100)
        # FindOpticalProbeHeight(1, 100)

        # Step to the specified die
        self.logger.info(f"[Prober Task] - Step to the specified die {die_num}. Issuing command 'StepToDie({die_num})'")
        self.signals.log_info.emit("Prober Task", f"Step to the specified die {die_num}", None)
        Prober.StepToDie(die_num)

        # Move hexapod and nano to height 50 um
        height = 80
        self.opt_if.set_probe_height(Probe.INPUT, height)
        self.opt_if.set_probe_height(Probe.OUTPUT, height)

        # Read the die data: die number, col, row
        self.model.die, self.model.die_col, self.model.die_row = self.get_die_as_col_row()

        # Set the current chuck and map to home
        self.set_chuck_home()
        self.set_map_home(self.model.die_col, self.model.die_row)

        # For reducing errors, read the chuck position
        self.model._chuck_x, self.model._chuck_y, self.model._chuck_z = self.read_chuck_position(unit="Microns", pos_ref="Home")

        self.logger.info(f"[Prober Task] - {pch('*', 20)} MOVING TO DIE COMPLETE {pch('*', 20)}")
        self.signals.log_info.emit("Prober Report", f"MOVING TO DIE COMPLETE", None)
        return self.model.die, self.model.die_col, self.model.die_row

    # ==================================================================================================================
    #
    # ==================================================================================================================

    def try_finding_light(self, input_power, output_power, threshold=-70):
        ran_in = [0, 5, -5, 10, -10, 15, -15, 20, -20, 25, 30, 35, 40, -25, -30, -35, -40]
        ran_out = ran_in
        # steps = 5

        input_power = self.msg_server.sendSciCommand("ReadOpticalProbePowerMeter", rparams='0')
        input_power = self.conv_result_power(input_power)

        output_power = self.msg_server.sendSciCommand("ReadOpticalProbePowerMeter", rparams='1')
        output_power = self.conv_result_power(output_power)

        for x_pos_1 in ran_in:
            for y_pos_1 in ran_in:
                try:
                    self.msg_server.sendSciCommand("MoveOpticalProbe",
                                                   rparams='0 %s %s R' % ((float(x_pos_1)), (float(y_pos_1))))
                except Exception as e:
                    self.write_log("error", "Can't move probe to (%s, %s)" % (x_pos_1, y_pos_1))
                    self.write_log("error", e)
                    continue

                for x_pos_2 in ran_out:
                    for y_pos_2 in ran_out:
                        self.write_log("debug",
                                       f"{self.formatter} Moving realtivly: Probe 1 X({float(x_pos_1)}) Y({float(y_pos_1)}) "
                                       f"| Probe 2  X({float(x_pos_2)}) Y({float(y_pos_2)}) | Power I:{input_power} O:{output_power}")

                        self.msg_server.sendSciCommand("MoveOpticalProbe",
                                                       rparams='1 %s %s R' % ((float(x_pos_2)), (float(y_pos_2))))

                        input_power = self.msg_server.sendSciCommand("ReadOpticalProbePowerMeter", rparams='0')
                        output_power = self.msg_server.sendSciCommand("ReadOpticalProbePowerMeter", rparams='1')
                        input_power = self.conv_result_power(input_power)
                        output_power = self.conv_result_power(output_power)

                        if (float(input_power) > -72) or (float(output_power) > -72):
                            try:
                                self.msg_server.sendSciCommand("AreaScan", rparams='1 1')
                                self.msg_server.sendSciCommand("RecenterOpticalProbe", rparams='0')
                                self.msg_server.sendSciCommand("RecenterOpticalProbe", rparams='1')
                                self.msg_server.sendSciCommand("AreaScan", rparams='1 1')
                                self.msg_server.sendSciCommand("RecenterOpticalProbe", rparams='0')
                                self.msg_server.sendSciCommand("RecenterOpticalProbe", rparams='1')
                                self.msg_server.sendSciCommand("AreaScan", rparams='1 1')
                                if (float(input_power) > threshold) or (float(output_power) > threshold):
                                    self.write_log("debug", f"Power I:{input_power} O:{output_power}. Continuing.")
                                    return True
                            except Exception as e:
                                self.write_log(f"warning {e}")

                        self.write_log("debug",
                                       f"{self.formatter} Moving back: Probe 1 X({(-1) * float(x_pos_1)}) Y({(-1) * float(y_pos_1)}) "
                                       f"| Probe 2  X({(-1) * float(x_pos_2)}) Y({(-1) * float(y_pos_2)}) | Power I:{input_power} O:{output_power}")
                        self.msg_server.sendSciCommand("MoveOpticalProbe", rparams='0 %s %s R' % (
                            ((-1) * float(x_pos_1)), ((-1) * float(y_pos_1))))
                        self.msg_server.sendSciCommand("MoveOpticalProbe", rparams='1 %s %s R' % (
                            ((-1) * float(x_pos_2)), ((-1) * float(y_pos_2))))

        self.write_log("warning", "No light found.")
        return False

    def store_hexapod_position():
        """
            Stores the hexpods and nanocube position for later retrieval
        """
        pass


    # msgServer.sendSciCommand("MoveOpticalProbe", rparams='0 %s %s R' % ( (-1)*(float(x_pos_1)), (-1)*(float(y_pos_1))))

    def get_hexapod_values(self):
        # before performing an area scan, store the current position
        try:
            motor_x_1, motor_y_1, motor_z_1, pzt_x_1, pzt_y_1, pzt_z_1 = self.msg_server.sendSciCommand(
                "ReadOpticalProbePos", rparams='0 H')
            motor_x_2, motor_y_2, motor_z_2, pzt_x_2, pzt_y_2, pzt_z_2 = self.msg_server.sendSciCommand(
                "ReadOpticalProbePos", rparams='1 H')
            self.write_log("info",
                           "([%s]: %s): Storing reference values for motor 1 (%s, %s, %s) Storing values for PZT 1 (%s, %s, %s). "
                           % (self.die_no, self.structure, motor_x_1, motor_y_1, motor_z_1, pzt_x_1, pzt_y_1, pzt_z_1)
                           )
            self.write_log("info",
                           "([%s]: %s): Storing reference values for motor 2 (%s, %s, %s) Storing values for PZT 2 (%s, %s, %s). "
                           % (self.die_no, self.structure, motor_x_2, motor_y_2, motor_z_2, pzt_x_2, pzt_y_2, pzt_z_2)
                           )
        except Exception as e:
            self.write_log("warning", "([%s]: %s): Can't store reference values for motor 1 and 2." % (
                self.die_no, self.structure))
            self.write_log("warning", e)

        motor_pos = {
            'motor_1': {
                'x': motor_x_1, 'y': motor_y_1, 'z': motor_z_1
            },
            'motor_2': {
                'x': motor_x_2, 'y': motor_y_2, 'z': motor_z_2
            }
        }

        pzt_pos = {
            'pzt_1': {
                'x': pzt_x_1, 'y': pzt_y_1, 'z': pzt_z_1
            },
            'pzt_2': {
                'x': pzt_x_2, 'y': pzt_y_2, 'z': pzt_z_2
            }
        }

        return motor_pos, pzt_pos

    def _write_debug(self, description, title=None, details=None):
        if details is None and title is None:
            self.logger.debug(f"{description}.")
            self.signals.log_debug.emit(None, description, None)
        elif details is not None and title is None:
            self.logger.debug(f"{description}: {details}")
            self.signals.log_debug.emit(None, description, details)
        elif details is None and title is not None:
            self.logger.debug(f"[{title}] - {description}")
            self.signals.log_debug.emit(None, description, None)
        else:
            self.logger.debug(f"[{title}] - {description}: {details}")
            self.signals.log_debug.emit(title, description, details)

    def _write_info(self, description, title=None, details=None):
        if details is None and title is None:
            self.logger.info(f"{description}.")
            self.signals.log_info.emit(None, description, None)
        elif details is not None and title is None:
            self.logger.info(f"{description}: {details}")
            self.signals.log_info.emit(None, description, details)
        elif details is None and title is not None:
            self.logger.info(f"[{title}] - {description}")
            self.signals.log_info.emit(None, description, None)
        else:
            self.logger.info(f"[{title}] {description}: {details}")
            self.signals.log_info.emit(title, description, details)

    def _write_warning(self, description, title=None, details=None):
        if details is None and title is None:
            self.logger.warning(f"{description}.")
            self.signals.log_warning.emit(None, description, None)
        elif details is not None and title is None:
            self.logger.warning(f"{description}: {details}")
            self.signals.log_warning.emit(None, description, details)
        elif details is None and title is not None:
            self.logger.warning(f"[{title}] - {description}")
            self.signals.log_warning.emit(None, description, None)
        else:
            self.logger.warning(f"[{title}] - {description}: {details}")
            self.signals.log_warning.emit(title, description, details)

    def _write_error(self, description, title=None, details=None):
        if details is None and title is None:
            self.logger.error(f"{description}.")
            self.signals.log_error.emit(None, description, None)
        elif details is not None and title is None:
            self.logger.error(f"{description}: {details}")
            self.signals.log_error.emit(None, description, details)
        elif details is None and title is not None:
            self.logger.error(f"[{title}] - {description}")
            self.signals.log_error.emit(None, description, None)
        else:
            self.logger.error(f"{title}. {description}: {details}")
            self.signals.log_error.emit(title, description, details)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def __del__(self):
        self.msg_server.__exit__()
        self.logger.info("Message Server closed!")
