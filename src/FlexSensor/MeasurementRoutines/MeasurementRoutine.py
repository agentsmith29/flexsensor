import logging
import time
import traceback
from datetime import datetime

import CaptDeviceControl as AD2Dev
import LaserControl as Laser
import mcpy
import pandas as pd
from PySide6.QtCore import Slot
from constants.FlexsensorConstants import Probe
from generics.generics import pch

import FlexSensor.Prober as Prober
from FlexSensor.FlexSensorConfig import FlexSensorConfig
from FlexSensor.MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
from FlexSensor.MeasurementData.Properties.AD2CaptDeviceProperties import AD2CaptDeviceProperties
from FlexSensor.MeasurementData.Properties.LaserProperties import LaserProperties
from FlexSensor.MeasurementData.Properties.MeasurementProperties import MPropertiesFindPeaks, \
    MeasurementProperties, WaveguidePropertiesMZI
from FlexSensor.MeasurementData.Properties.WaferProperties import WaferProperties
from FlexSensor.MeasurementRoutines.BasemeasurementRoutine import BaseMeasurementRoutine
from FlexSensor.generics.VASInputFileParser import VASInputFileParser, Structure


class MeasurementRoutine(BaseMeasurementRoutine):

    def __init__(self, laser: Laser, ad2device: AD2Dev, prober: Prober.Controller,
                 config: FlexSensorConfig):
        super().__init__(laser, ad2device, prober, config)

        self.logger = logging.getLogger("Measurement Routine")
        # The signals for connecting to the UI

        self.parsed_file = VASInputFileParser()

        selected_file, self.grouped_structures, self.bookmarks = self.parsed_file.read_file(
            input_file=self.config.wafer_config.structure_file.get()
        )
        self.number_of_structures = self.parsed_file.num_of_structs
        self.number_of_runs = self.parsed_file.num_of_runs

        self.config.wafer_config.structure_file.set(selected_file)
        # We need to connect two signals:
        # Connect the signal if a wavelength sweep starts (from the laser) to a signal that tells our oscilloscope
        # to start capturing!
        # self.laser.signals.wavelength_sweep_running.connect(self.ad2device.on_ad2_set_acquisition_changed)

        # Some intermediate Data
        self.columns = ["wafer_nr", "die_nr", "chuck_col", "chuck_row", "timestamp", "structure_name",
                        "reps", "structure_x_in", "structure_y_in", "structure_x_out",
                        "structure_y_out", "measure_time", "timestamps", "captured_values"]
        self.siph_data = pd.DataFrame(columns=self.columns)
        self.siph_data['captured_values'] = self.siph_data['captured_values'].astype(object)

        self.initialization()

    def initialization(self):
        self.probe_height = 80

        self.logger.info(
            f"Init Prober Class. Number of runs per die: {self.number_of_runs}, dies {self.config.wafer_config.dies.get()}\n"
            f"Measurement CVS File = {self.config.wafer_config.measurement_output}\n"
            f"Measurement Mat File = {self.config.wafer_config.measurement_mat_file}")

    @Slot()
    def run(self):
        self.logger.info(f"<< Input file {self.config.wafer_config.structure_file.get()}")
        self.logger.info(f">> Working directory {self.config.output_directory.get()}")
        self.logger.info(f">> Log File {self.config.wafer_config.log_file.get()}")
        self.logger.info(f">> Measurements CVS File {self.config.wafer_config.measurement_output.get()}")
        self.logger.info(f">> Measurements Mat File {self.config.wafer_config.measurement_mat_file.get()}")
        self.logger.info(f">> KLayout Bookmark file {self.config.wafer_config.bookmark_file.get()}")
        self.logger.info(f">> Scope Image File {self.config.wafer_config.scope_image_file.get()}")

        # as long as the connection was successful, we can send some commands.
        # if it was not successful, an exception is thrown.

        self.logger.warning("*** Check safe height. Contact height must be set.***")
        # SCI commands return a namedtuple if multiple values are returned.
        # ReportKernelVersion returns a version number and a description.
        # You can acess the return values by name or by indexing the tuple.
        self.logger.info("Everything is set up, starting measuring.")

        self._routine()

    def _routine(self):
        try:
            # Initialize the devices
            self._init_prober_signals()
            # self._init_laser_signals()
            # self._init_ad2device_signals()

            self._write_info(
                f"{pch('=', 50)} Starting measurement {pch('=', 50)}")

            # === Check contact height
            print(self.prober)
            contact, overtravel, align_dist, sep_dis, search_gap = self.prober.check_contact_height_set()

            for die_idx, die_no in enumerate(self.config.wafer_config.dies.get()):
                # Move to die
                self.write_log("info", f"Processing die {die_no} (#{die_idx})")
                self.die_no, self.chuck_col, self.chuck_row = self.prober.move_to_die(die_no)

                if self.die_no is not None and self.chuck_col is not None and self.chuck_row is not None:
                    self.write_log("info", f"Chuck moved to home position. Die {self.die_no} "
                                           f"(Col: {self.chuck_col}, Row: {self.chuck_row})")
                else:
                    # STOP SiPh-Tools
                    self.write_log("fatal", "Chuck could not be moved to home position. Script will be stopped!")
                    raise Exception("Chuck could not be moved to home position. Script will be stopped!")

                # Go to the home position
                self.write_log("info", "Move chuck to home position (0, 0)")
                self.prober.move_chuck(0, 0)

                # Iterate through the list of structures
                for idx_groups, self.groups in enumerate(self.grouped_structures):

                    structures: dict = self.grouped_structures[self.groups]
                    idx_struct = 0
                    self.write_log("info", f"New structure group ({idx_groups}): "
                                           f"{self.groups}. {len(structures)} structures in group.")

                    while idx_struct < len(structures):
                        structure = list(structures.values())[idx_struct]
                        self._measure_structure(die_no, structure, idx_struct)
                        idx_struct += 1
                        continue


        except Exception as e:
            self._write_error(title="Prober initialization error", desc="Could not connect or initialize prober",
                              e=e, tb=traceback)

    # ==================================================================================================================
    # The individual steps for the Measurement Routine
    # If implementing multiple routines, and the steps may occure multiple times, move them to
    # the base class instead of reimplementing/copying!
    # ==================================================================================================================
    def _step_place_input_probe(self, structure: Structure, fmt):
        """
            Places the chuck, thus the input probe, such that the probe is on the correct position.
            Move the chuck to the given position. Since the input probe stays on the same position,
            the probe is therefore on the correct input position.
        """
        x, y = (structure.x_in, structure.y_in)
        self.write_log("info", f"{fmt} Move input probe/chuck to X: {x}, Y: {y}.")
        self.prober.move_chuck(x, y)
        chuck_x, chuck_y, chuck_z = self.prober.read_chuck_position(unit="Microns", pos_ref="Home")
        self.write_log("info", f"{fmt} Input probe/chuck at position X: {chuck_x}, Y: {chuck_y}, Z: {chuck_z}.")
        return chuck_x, chuck_y, chuck_z

    def _step_place_output_probe(self, structure, fmt, safe_dist: float = 50):
        x, y = (structure.x_out, structure.y_out)
        diff_x, diff_y = (structure.in_out_diff_x, structure.in_out_diff_y)
        self.write_log("info", f"{fmt} Move second probe to x: {x}, y: {y}) - Difference x: {diff_x}, y: {diff_y}")

        # TODO: CHeck if the structure require a reposition of the probe
        move_probe2 = True

        if self.structure.in_out_diff_x > safe_dist and move_probe2:
            self.write_log("debug",
                           f"{fmt} Optical probes in safe distance {x > safe_dist}. Moving output probe x:{diff_x}, y: {diff_y}.")
            self.prober.opt_if.move_optical_probe(Probe.OUTPUT, diff_x, diff_y)
        elif self.structure.in_out_diff_x < safe_dist:
            raise Exception(f"Optical Probe Home not safe! Difference in x-direction < {safe_dist} um.")
        else:
            self.write_log("warning", f"Optical Probe not moved. Movement for probe disabled: {move_probe2}")

    def _step_set_probes_to_measurement_height(self, height, fmt):
        try:
            self.write_log("info", f"{fmt} Setting probe heights to {height} um")
            self.prober.opt_if.set_probe_height(Probe.INPUT, height)
            self.prober.opt_if.set_probe_height(Probe.OUTPUT, height)
            # self.msg_server.sendSciCommand("FindOpticalProbeHeight",
            #                               rparams='0 %s' % self.probe_height)
            # self.msg_server.sendSciCommand("FindOpticalProbeHeight",
            #                               rparams='1 %s' % self.probe_height)
        except Exception as e:
            self.write_log("error",
                           f"{fmt} Cannot set probe height to {height}. {e}")
            self.signals.error.emit((
                type(e), f"Cannot set probe height to {height}. {e}",
                traceback.format_exc()
            ))
            raise e

    def _step_snap_image(self, scope_file, fmt):
        # Here we adapt filename of the scope by passing the correct keywords
        try:
            self.write_log("info", f"{fmt} Saving scope image to {scope_file}")
            self.prober.snap_image("eVue2", scope_file, 2)
        except Exception as e:
            self.logger.warning(f"{fmt} Cannot save scope image to {scope_file}: {e}\n\n"
                                f"{traceback.format_exc()}")

            self.signals.warning.emit(type(e),
                                      f"Cannot save scope image to {scope_file}. {e}",
                                      traceback.format_exc())

    def _step_search_for_light(self, fmt):
        # TODO: Handle if we cannot find the light
        self.logger.info(f"{fmt} Searching for light.")
        self.signals.write_log.emit("info", "Searching for light.")
        input_power, output_power = self.prober.opt_if.search_for_light()
        if input_power is None or output_power is None:
            self.logger.warning(f"{fmt} Cannot find light. Something went wrong.")
            self.signals.warning.emit("warning", "Cannot find light. Something went wrong.", "")
            raise Exception('Cannot find light.')
        else:
            self.logger.info(f"{fmt} Light found. Input Power: {input_power} dBm. Output Power: {output_power} dBm")
            self.logger.info(f"{fmt} Light found. Input Power: {input_power} dBm. Output Power: {output_power} dBm")
            self.signals.write_log.emit("info",
                                        "Light found. Input Power: {input_power} dBm. Output Power: {output_power} dBm")

    def _step_capture_transmission(self, rep, fmt):
        self.logger.info(f"{fmt} Setting up AD2. This may take a while, please wait...")
        self.signals.write_log.emit("info", "Setting up oscilloscope.")

        #if not self.ad2device.connect_device(0):
        #    self.logger.error(f"{fmt} Could not setup ad2 device.")
        #    self.signals.error.emit("error", "Could not setup ad2 device.", "")
        #    raise Exception("Could not setup ad2 device. Script will be stopped!")

        # *******************
        # Start the measurement
        #self.laser.start_wavelength_sweep()
        #time.sleep(1)
        #while self.ad2device.model.capturing_finished == False:
        #    print(f"awaiting: {self.ad2device.model.capturing_finished}")
        #    time.sleep(1)

        #captured_values = self.ad2device.model.recorded_samples  # Just starts an endless loop
        #print(len(captured_values))
        #measure_time = self.ad2device.model.recording_time
        self.laser.start_wavelength_sweep.emit(self.laser.model.sweep_start_wavelength,
                                          self.laser.model.sweep_stop_wavelength)
        while self.laser.model.wavelength_sweep_running:
            self.logger.info(f"{fmt} Wavelength sweep running. Waiting for sweep to finish.")
            time.sleep(1)
        measure_time = self.ad2device.model.capturing_information.recording_time
        captured_values = self.ad2device.model.capturing_information.recorded_samples

        self.write_log("info", f"{self.formatter} Finished data acquisition: {len(captured_values)}. Took {round(measure_time, 5)} seconds.")
        return measure_time, captured_values

    def _step_create_MeasuredSignal(self, data: pd.DataFrame, data_raw: list, wafer_properties: WaferProperties):
        # timestamp, measure_time, time_stamps, amplitude
      
        try:
            cur_measured_signal = SingleMeasuredData(
                laser_properties=LaserProperties(
                mcpy.Rectangular(2, 0.01, unit='nm/s'),
                mcpy.Rectangular(2, 0.01, unit='nm/s'),
                mcpy.Rectangular(0.5, 0.01, unit='nm/s^2'),
                (mcpy.Rectangular(835, 0.01, unit='nm'), mcpy.Rectangular(870, 0.01, unit='nm'))),
                ad2_properties=AD2CaptDeviceProperties( 0, 0, 0, 0, 0),
                wafer_properties=wafer_properties,
                waveguide_properties=WaveguidePropertiesMZI(
                    length1=mcpy.Rectangular(10e6, 20, unit='nm'),
                    length2=mcpy.Rectangular(10.38e6, 20, unit='nm'),
                    width=mcpy.Rectangular(550, 20, unit='nm'),
                    height=mcpy.Rectangular(625, 2.405, unit='nm')),
                measurement_properties=MeasurementProperties(
                    MPropertiesFindPeaks(0.1, 10000, None)
                ),
                timestamp=data['timestamp'],
                measurement_data=data_raw
            )

            # cur_measured_signal.set_prober_properties(
            #     self.vaut_config.wafer_nr,
            #     self.die_no,
            #     self.chuck_col,
            #     self.chuck_row
            # )
            # cur_measured_signal.set_structure_properties(self.structure)
            # cur_measured_signal.set_ad2_properties(
            #     self.vaut_config.ad2_device_config.get_sample_rate(),
            #     self.vaut_config.ad2_device_config.get_total_samples())
            #
            # cur_measured_signal.set_laser_properties(
            #     self.vaut_config.laser_config.get_wavelength_range(),
            #     self.vaut_config.laser_config.get_velocity(),
            #     self.vaut_config.laser_config.get_acceleration())

            return cur_measured_signal

        except Exception as e:
            self.write_log("error", f"Could not create MeasuredSignal instance from data: {e}")
            self.signals.error.emit((type(e),
                                     f"Could not create MeasuredSignal instance from data: {e}",
                                     traceback.format_exc()))
            raise e

    # Routine for measuring one structure
    def _measure_structure(self, die_no: int, structure: Structure, structure_idx: int):
        """Routine for measuring one structure

        """
        self.structure: Structure = structure
        self.formatter = f"[Measurement. Die {die_no}]: {self.structure.name} |"
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')

        if not self.structure.enabled:
            self.write_log("info", f"Structure {self.structure.name} is disabled, skipping!")
            return

        self.write_log("info", f"{self.formatter} Processing structure {self.structure.name}.")
        # Report the current structure information to the frontend
        self.signals.report_info.emit({
            "die_no": self.die_no, "chuck_col": self.chuck_col,
            "chuck_row": self.chuck_row, "structure": self.structure.name,
            "repetition": self.structure.repetitions
        })
        self.write_log("info", f"{self.formatter} "
                               f"die_no: {self.die_no}, chuck_col: {self.chuck_col}, "
                               f"chuck_row: {self.chuck_row}, structure: {self.structure.name}, "
                               f"repetition: {self.structure.repetitions}"
                       )

        # 1. Move the first probe/chuck
        self._step_place_input_probe(self.structure, self.formatter)

        # 2. Move the second probe
        self._step_place_output_probe(self.structure, self.formatter)

        # 3. Setting the probe height to 80 um
        self._step_set_probes_to_measurement_height(80, self.formatter)

        # 4. Snap an image
        # Create the correct file for the scope image
        # self.vaut_config.wafer_config.get_scope_image_file().set_obj(
        #    keywords={"{die}": self.die_no, "{structure}": self.structure.name, "{it}": 1})
        self._step_snap_image(
            str(self.config.wafer_config.scope_image_file.get()).
            replace("{die}", str(self.die_no)).
            replace("{structure}", str(self.structure.name)), self.formatter)

        # Search for the light
        self._step_search_for_light(self.formatter)

        amplitude = []
        time_stamps = []
        rep = 1

        while rep <= self.structure.repetitions:
            # *******************
            # Stop the measurement
            # For displaying the data in the GUI
            measure_time, captured_values = self._step_capture_transmission(rep, self.formatter)
            data = [[
                self.config.wafer_number.get(), self.die_no, self.chuck_col,
                self.chuck_row, timestamp, str(self.structure), rep,
                self.structure.x_in, self.structure.y_in,
                self.structure.x_out, self.structure.y_out,
                measure_time, str(time_stamps), captured_values
            ]]
            self.siph_data = pd.concat([self.siph_data, pd.DataFrame(data, columns=self.columns)])

            try:
                self.siph_data.to_csv(str(self.config.wafer_config.measurement_output.get()))
                self.siph_data.to_excel(
                    str(self.config.wafer_config.get_measurement_output()).replace('csv', 'xlsx'))
            except Exception as e:
                self._write_error("Write SiPh", f"Could not write sphi data to file "
                                                f"{self.config.wafer_config.measurement_output.get()}", e,
                                  traceback)
                self.signals.error.emit((type(e),
                                         f"Could not write sphi data to file "
                                         f"{self.config.wafer_config.measurement_output.get()}: {e}",
                                         traceback.format_exc()))

            wafer_properties = WaferProperties(
                wafer_number=self.config.wafer_number.get(),
                structure_name=self.structure.name,
                die_nr=self.die_no,
                chuck_col=self.chuck_col,
                chuck_row=self.chuck_row,
                structure_in=(self.structure.x_in, self.structure.y_in),
                structure_out=(self.structure.x_out, self.structure.y_out),
                repetitions=rep)
           
            #cur_measured_signal = self._step_create_MeasuredSignal(
            #    self.siph_data,
            #    captured_values,
            #    wafer_properties)

            #cur_measured_signal._save_mat_file(
            #    filename=self.config.wafer_config.get_measurement_mat_file(keywords={"{die}": self.die_no,
            #                                                                              "{structure}": self.structure.name,
            #                                                                              "{it}": f"rep_{rep + 1}"}).absolute
            #)


            rep += 1
            self.logger.info(f"Repetition {rep}/{self.structure.repetitions} measured successfully!")
            #self.signals.routine_iteration_finished.emit(cur_measured_signal, rep)
            # Report the progress to the frontend
        self.write_log("info", "[OK] Continuing with next structure.")
        # idx_struct = idx_struct + 1
