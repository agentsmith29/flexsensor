import logging

from Prober.model.OpticalInterfaceModel import OpticalInterfaceModel
from Prober.model.OpticalInterfaceStoredData import OpticalInterfaceStoredData
from constants.FlexsensorConstants import Probe
from generics.generics import pch













class OpticalInterface(object):

    def __init__(self, prober_signals, msg_server):
        self.stored = OpticalInterfaceStoredData()
        self.signals = prober_signals
        self.msg_server = msg_server
        self.logger = logging.getLogger("Optical Interface")
        self.logger.info("Optical Interface initialized")

    # ==================================================================================================================
    # pythonized api calls
    # ==================================================================================================================

    def enable_flight_height_control(self, enable_in=True, enable_out=True):
        # Disable Flight Height Control
        for probe_num, val in enumerate((int(enable_in), int(enable_out))):
            cmd = 'TrackOpticalProbeHeight'
            rparams = f"{probe_num} {val}"

            enable = bool(val)
            enable_desc = 'Enable' if enable else 'Disable'
            probe_desc = 'first probe/input probe' if probe_num == 0 else 'second probe/output probe'
            command_desc = f'{cmd}({rparams})'
            self.logger.info(f"[OptIF Task] - {enable_desc} `Flight Height Control` "
                             f"for {probe_desc}. Issuing command '{command_desc}'")
            self.signals.log_info.emit("OptIF", f" {enable_desc} 'Flight Height Control' "
                                                f"for {probe_desc}.", None)
            self.msg_server.sendSciCommand(cmd, rparams=rparams)

    def set_probe_height(self, probe: int, height):
        cmd = 'FindOpticalProbeHeight'
        rparams = f"{probe} {height}"

        probe_desc = 'first probe/input probe' if probe == 0 else 'second probe/output probe'
        command_desc = f'{cmd}({rparams})'

        self.logger.info(f"[OptIF  Task] - Move {probe_desc} height to {height} um. "
                         f"Issuing command '{command_desc}'")
        self.signals.log_info.emit("OptIF  Task", f" Move {probe_desc} height to {height} um.", None)
        self.msg_server.sendSciCommand(cmd, rparams=rparams)

    def move_optical_probe(self, probe: int, x, y, pos_ref='H'):
        """
        Move selected probe motor in XY.
        :param probe 0=Input, 1=Output (I)
        :param x motor command [um] (D)
        :param y motor command [um] (D)
        :param pos_ref R=Relative, H=Home, Z=Zero (C)
        """
        cmd = 'MoveOpticalProbe'
        rparams = f"{probe} {x} {y} {pos_ref}"
        command_desc = f'{cmd}({rparams})'
        self.logger.info(f"[OptIF  Task] - Move selected probe motor. "
                         f"Issuing command '{command_desc}'")
        self.msg_server.sendSciCommand(cmd, rparams=rparams)

    def move_pzt(self, probe: int, x, y, z, pos_ref='H'):
        """
        Pythonized command for SiP Remote Interface 'MovePZT'
        Move selected PZT.
        :param probe: 0=Input, 1=Output (I)
        :param x: x PZT command [um] (D)
        :param y: y PZT command [um] (D)
        :param z: z PZT command [um] (D)
        :param pos_ref: PosRef R=Relative, H=Home, Z=Zero (C)
        """
        cmd = "MovePZT"
        rparams = f"{probe} {x} {y} {z} {pos_ref}"
        self.logger.info(f"[OptIF  Task] - Move selected PZT.")
        return self._send_command(cmd, rparams=rparams,
                                  desc=f"{cmd}(probe={probe}, x={x}, y={y}, z={z}, posref={pos_ref})")

    def recenter_optical_probe(self, probe: int):
        cmd = 'RecenterOpticalProbe'
        rparams = f"{probe}"

        probe_desc = 'first probe/input probe' if probe == 0 else 'second probe/output probe'
        command_desc = f'{cmd}({rparams})'

        self.logger.info(f"[OptIF  Task] - Recenter {probe_desc}. "
                         f"Issuing command '{command_desc}'")
        self.signals.log_info.emit("OptIF  Task", f"Recenter {probe_desc}.", None)

        self.msg_server.sendSciCommand(cmd, rparams=rparams)

    def area_scan(self, probe_in: bool = True, probe_out: bool = True):
        cmd = 'AreaScan'
        probe_in, probe_out = (int(probe_in), int(probe_out))
        rparams = f"{probe_in} {probe_out}"

        if probe_in == 1 and probe_out == 1:
            probe_desc = 'input and output probe'
        elif probe_in == 1 and probe_out == 0:
            probe_desc = 'first probe/input probe'
        elif probe_in == 0 and probe_out == 1:
            probe_desc = 'second probe/output probe'
        else:
            raise ValueError("area_scan requires at least one probe to be selected.")

        command_desc = f'{cmd}({rparams})'

        self.logger.info(f"[OptIF  Task] - Performing area scan on {probe_desc}. "
                         f"Issuing command '{command_desc}'")
        self.signals.log_info.emit("OptIF  Task", f"Performing area scan on {probe_desc}", None)

        x_1, x_2, y_1, y_2, input_power, output_power = self.msg_server.sendSciCommand(cmd, rparams=rparams)
        return x_1, x_2, y_1, y_2, self.conv_pwr(input_power), self.conv_pwr(output_power)

    def set_optical_probe_home(self, probe: int) -> (int, int, int, int, int, int):
        cmd = 'SetOpticalProbeHome'
        rparams = f"{probe}"
        return self.msg_server.sendSciCommand(cmd, rparams=rparams)

    def read_optical_probe_pos(self, probe, pos_ref='H') -> (float, float, float, float, float, float):
        """
        Pythonized command for SiP Remote Interface 'ReadOpticalProbePos'
        Read optical probe position.
        :param probe: 0=Input, 1=Output (I)
        :param pos_ref: H=Home, Z=Zero (C)
        :return:
        x1: x motor position [um]
        y1: y motor position [um]
        z1: z motor position [um]
        x2: x motor PZT [um]
        y2: y PZT position [um]
        z2: x PZT position [um]
        """
        cmd = "ReadOpticalProbePos"
        rparams = f"{probe} {pos_ref}"
        self.logger.info(f"[OptIF  Task] - Reading optical probe position. ")
        return self._send_command(cmd, rparams=rparams, desc=f"{cmd}(probe={probe}, posref={pos_ref})")


    # ==================================================================================================================
    # Custom implementations I
    # ==================================================================================================================
    def _send_command(self, cmd: str, rparams: str = None, desc: str = None):

        issuing_command = f'{cmd}({rparams})'
        if desc is not None:
            self.logger.debug(f"Issuing command {desc} -> '{issuing_command}'")
        else:
            self.logger.debug(f"Issuing command '{issuing_command}'")

        self.signals.log_info.emit("OptIF  Task", f"Issuing command '{issuing_command}'", None)
        r = self.msg_server.sendSciCommand(cmd, rparams=rparams)
        self.logger.debug(f"Command returned '{r}'")
        return r

    # ==================================================================================================================
    # Custom implementations II
    # ==================================================================================================================
    def conv_pwr(self, power: list | str | float | int) -> float:
            """
                Area scan return different types for the power values, this function can convert it.
            """
            try:
                if isinstance(power, list):
                    power = float(power[0])
                elif isinstance(power, str):
                    if "na" == power.lower:
                        power = -80
                    else:
                        power = float(power)
                else:
                    power = float(power)
            except Exception as e:
                power = -80
                print(f"Cant convert <{power}>: {e}")
            return float(power)

    def _recenter_and_scan(self) -> (float, float, float, float, float, float):
        self.recenter_optical_probe(Probe.INPUT)
        self.recenter_optical_probe(Probe.OUTPUT)
        x_1, x_2, y_1, y_2, input_power, output_power = self.area_scan(True, True)
        return float(x_1), float(x_2), float(y_1), float(y_2), self.conv_pwr(input_power), self.conv_pwr(
            output_power)

    def search_for_light(self, threshold: float = -70, threshold_areascan: float = -60, retries: float = 3):
        self.logger.debug(f"[OptIF  Task] - {pch('*', 20)} Search for light {pch('*', 20)}")
        self.signals.log_debug.emit("OptIF  Task", f"*** Search for light ***", None)

        # Recenter the probes, perform an area scan, recenter again.
        self.logger.info(f"[OptIF  Task] - Recenter optical probes and performing area scan (1/2).")
        self.signals.log_info.emit("OptIF  Task", f"Recenter optical probes (1/2).", None)
        self._recenter_and_scan()

        self.logger.info(f"[OptIF  Task] - Recenter optical probes and performing area scan (2/2).")
        self.signals.log_info.emit("OptIF  Task", f"Recenter optical probes (2/2).", None)
        x_1, x_2, y_1, y_2, input_power, output_power = self._recenter_and_scan()

        # Now we need to verify the power
        self.logger.info(f"[OptIF  Task] - Verifying power. Probe input power: {input_power}. "
                         f"Probe output power {output_power}. "
                         f"Abortion criteria is {threshold}/{threshold_areascan} or {retries} retries.")
        self.signals.log_info.emit("OptIF  Task", f"Probe input power: {input_power}. "
                                                  f"Probe output power {output_power}.", None)
        while (
                ((input_power < threshold_areascan and output_power >= threshold) or
                 (output_power < threshold_areascan and input_power >= threshold)) and
                retries > 0
        ):
            self.logger.info(f"[OptIF  Task] - Input power ({input_power}) or output power ({output_power}) "
                             f"too low but signal found. Trying area scan again ({retries - 1} "
                             f"retrie(s) left). Threshold is {threshold_areascan}")
            self.signals.log_info.emit("OptIF  Task",
                                       f"Input power ({input_power}) or output power ({output_power}) "
                                       f"too low but signal found. ", None)
            x_1, x_2, y_1, y_2, input_power, output_power = self._recenter_and_scan()
            retries -= 1

        self.logger.debug(f"[OptIF  Task] - {pch('*', 20)} Search for light completed {pch('*', 20)}")
        self.signals.log_debug.emit("OptIF  Task", f"*** Search for light completed***", None)
        return input_power, output_power

    # ==================================================================================================================
    # Store and load functions
    # ==================================================================================================================
    def store_optical_probe_motor_pos(self) -> (float, float, float, float, float, float):
        """
        Stores the current motor position of the optical probe .
        """
        self.stored.motor_in_x, self.stored.motor_in_y, self.stored.motor_in_z, \
            _, _, _ = self.read_optical_probe_pos(0)

        self.stored.motor_out_x, self.stored.motor_out_y, self.stored.motor_out_z, \
            _, _, _ = self.read_optical_probe_pos(1)

    def store_optical_probe_pzt_pos(self) -> (float, float, float, float, float, float):
        """
        Stores the current PZT position of the optical probe .
        """
        _, _, _, self.stored.pzt_in_x, self.stored.pzt_in_y, self.stored.pzt_in_z = self.read_optical_probe_pos(0)

        _, _, _, self.stored.pzt_out_x, self.stored.pzt_out_y, self.stored.pzt_out_z = self.read_optical_probe_pos(1)

    def store_optical_probe_pos(self) -> (float, float, float, float, float, float):
        """
        Stores the current motor position of the optical probe .
        """
        self.stored.motor_in_x, self.stored.motor_in_y, self.stored.motor_in_z, \
        self.stored.pzt_in_x, self.stored.pzt_in_y, self.stored.pzt_in_z = self.read_optical_probe_pos(0)

        self.stored.motor_out_x, self.stored.motor_out_y, self.stored.motor_out_z, \
        self.stored.pzt_out_x, self.stored.pzt_out_y, self.stored.pzt_out_z = self.read_optical_probe_pos(1)

    def restore_optical_probe_motor_pos(self, probe: int) -> (float, float, float, float, float, float):
        self.move_optical_probe(probe, self.stored.motor_in_x, self.stored.motor_in_y, pos_ref='H')
        return self.read_optical_probe_pos(probe)

    def restore_optical_probe_pzt_pos(self, probe: int) -> (float, float, float, float, float, float):
        self.move_pzt(probe, self.stored.pzt_in_x, self.stored.pzt_in_y, self.stored.pzt_in_z, pos_ref='H')
        return self.read_optical_probe_pos(probe)

    # ==================================================================================================================
    # Store and load functions
    # ==================================================================================================================

