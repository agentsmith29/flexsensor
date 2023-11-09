import logging

from PySide6.QtCore import QThread

import ConfigHandler as Config
import Laser as Laser
import AD2CaptDevice as AD2Dev
import Prober as Prober
import MeasurementEvaluationTool

from MainWindow.model.MainThreadModel import MainThreadModel
from MeasurementRoutines.MeasurementRoutine import MeasurementRoutine
from Prober.controller.ProberController import ProberController


class MainThreadController(object):
    def __init__(self, model: MainThreadModel):
        self.logger = logging.getLogger("MainThread")
        self._model = model

        # self.model._laser_controller.connect_device(self._vaut_config.laser_config.get_port())

        mypath = (
            r'F:\measurements_06032022\measurements_06032022\mea_mzi2_2_2022_03_06\T40741W177G0\MaskARY1_Jakob\measurement')

        # Device init: Connect signals and slots
        self._device_initialization()

        # Load the measurement routine
        self.model.measurement_routine = self._load_measurement_routine()

        # Thread for the measurement routine
        self.measurement_thread = QThread()

        # Create the working folders
        self._create_working_folders()

    @property
    def model(self) -> MainThreadModel:
        return self._model

    def start_measurement_routine(self):
        # 1. Create all working folders
        self._create_working_folders()
        self._move_measurement_routine_thread(self.model.measurement_routine)
        self.measurement_thread.start()
        self.logger.info("Started worker thread for running the measurement routine.")

        if self.measurement_thread.isRunning():
            self.logger.debug("Thread is running.")

    def _create_working_folders(self):
        """Creates all working folders to store the measurement data.
        """
        self.model.vaut_config.setup_folders()

    def _move_measurement_routine_thread(self, measurement_routine):
        measurement_routine.moveToThread(self.measurement_thread)
        self.measurement_thread.started.connect(measurement_routine.run)
        self.logger.debug("Moved worker/measurement routine to thread and connected the signals.")


    def _load_measurement_routine(self) -> MeasurementRoutine:
        """
            Loads the measurement routine and initializes it.

            Returns:
                MeasurementRoutine: The measurement routine.

            Raises:
                Exception: If some or all devices have not been initialized.
        """
        if not self.device_are_init:
            raise Exception("Some or all devices have not been initialized. First call `_device_initialization()`!")

        measurement_routine = MeasurementRoutine(
            self.model.laser_controller,
            self.model.ad2_controller,
            self.model.prober_controller,
            self.model.vaut_config)
        self.logger.debug("Initialized MeasurementRoutine.")
        return measurement_routine

    def _device_initialization(self):
        """
            Initializes all devices and connects the signals and slots.
        """
        self.model.ad2_controller.connect_device(0)
        # # Connect the required signals and slots
        # self.model.laser_model.signals.laser_ready_for_sweep_changed.connect(
        #     self.model.ad2_controller.start_capture_flag)
        #
        # self.model.ad2_model.signals.device_ready_changed.connect(
        #     self.model.laser_controller.start_wavelength_sweep)
        #
        # self.model.laser_model.signals.wavelength_sweep_running_changed.connect(
        #     self.model.ad2_controller.set_ad2_acq_status)

        self.device_are_init = True
