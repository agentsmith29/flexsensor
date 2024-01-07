import logging

from PySide6.QtCore import QThread, Signal

import confighandler
import LaserControl as Laser
import CaptDeviceControl as AD2Dev

import Prober as Prober
import MeasurementEvaluationTool

from ..model.MainThreadModel import MainThreadModel
from FlexSensor.MeasurementRoutines.MeasurementRoutine import MeasurementRoutine
from Prober.controller.ProberController import ProberController

from ...FSBase import FSBase


class MainThreadController(FSBase, object):

    on_start_laser_sweep = Signal(name='on_start_laser_sweep')

    def __init__(self, model: MainThreadModel,
                 enable_log: bool = True, log_level: int = logging.DEBUG, log_file: str = "flexsensor.log"):
        super().__init__()

        self._model = model

        self._enable_log = enable_log
        self._log_file = log_file
        self._log_level = log_level

        self.logger = self.create_new_logger(self.name,
                                             enabled=self.enable_log, level=self.log_level)

        self.model.ad2_model = AD2Dev.Model(self.model.config.captdev_config)
        self.model.ad2_controller = AD2Dev.Controller(self.model.ad2_model, self.model.start_capture_flag)
        self.model.ad2_window = AD2Dev.View(self.model.ad2_model, self.model.ad2_controller)

        # Devices
        self.model.laser_model = Laser.Model(self.model.config.laser_config)
        self.model.laser_controller = Laser.Controller(self.model.laser_model, self.model.start_capture_flag,
                                                       module_log_level=logging.DEBUG)

        self.model.laser_window = Laser.View(self.model.laser_model, self.model.laser_controller)
        self.model.laser_controller.connect_capture_device(self.model.ad2_controller)


        self.model.prober_model = Prober.Model(self.model.config)
        self.model.prober_controller = Prober.Controller(self.model.prober_model)
        self.model.prober_window = Prober.ControlWindow(self.model.prober_model, self.model.prober_controller)

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

    @property
    def enable_log(self) -> bool:
        return self._enable_log

    @property
    def log_file(self) -> str:
        return self._log_file

    @property
    def log_level(self) -> int:
        return self._log_level

    def start_measurement_routine(self):
        # 1. Create all working folders
        self._create_working_folders()
        self._move_measurement_routine_thread(self.model.measurement_routine)
        self.measurement_thread.start()
        self.logger.info("Started worker thread for running the measurement routine.")

        if self.measurement_thread.isRunning():
            self.logger.debug("Thread is running.")

    def _on_start_laser_sweep_emitted(self):
        self.logger.debug("Start laser sweep emitted.")

    def _create_working_folders(self):
        """Creates all working folders to store the measurement data.
        """
        pass
        # self.model.config.setup_folders()

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
        # if not self.device_are_init:
        #    raise Exception("Some or all devices have not been initialized. First call `_device_initialization()`!")

        measurement_routine = MeasurementRoutine(
            self.model.laser_controller,
            self.model.ad2_controller,
            self.model.prober_controller,
            self.model.config)
        self.logger.debug("Initialized MeasurementRoutine.")
        return measurement_routine

    def _device_initialization(self):
        """
            Initializes all devices and connects the signals and slots.
        """
        # self.model.ad2_controller.connect_device(0)
        # # Connect the required signals and slots
        # self.model.laser_model.signals.laser_ready_for_sweep_changed.connect(
        #     self.model.ad2_controller.start_capture_flag)
        #
        # self.model.ad2_model.signals.device_ready_changed.connect(
        #     self.model.laser_controller.start_wavelength_sweep)
        #
        # self.model.laser_model.signals.wavelength_sweep_running_changed.connect(
        #     self.model.ad2_controller.set_ad2_acq_status)

        self.device_are_init = False
