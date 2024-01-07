import logging

#from LaserControlOld.controller.BaseLaserController import BaseLaserController
from PySide6.QtCore import QObject, QThread, Slot

#from AD2CaptDevice.controller.AD2CaptDeviceController import AD2CaptDeviceController
#from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
#from Laser.LaserControl.controller import BaseLaserController

import CaptDeviceControl as CaptDevice
import LaserControl as Laser
import confighandler as Config

from FlexSensor.FSBase import FSBase
from FlexSensor.FlexSensorConfig import FlexSensorConfig
from FlexSensor.Prober.controller.ProberController import ProberController
from FlexSensor.MeasurementRoutines.WorkerSignals import WorkerSignals


class BaseMeasurementRoutine(QObject, FSBase):

    def __init__(self, laser: Laser.Controller, ad2device: CaptDevice.Controller, prober: ProberController, config: FlexSensorConfig):
        super().__init__()
        self.logger = self.create_new_logger(self.name)
        self.config = config

        self.ad2device: CaptDevice.Controller = ad2device
        self.laser: Laser.Controller = laser
        self.prober: ProberController = prober
        self.logger.debug(f"{self.prober.report_kernel_version()}")
        print(self.prober)
        
        self.prober_thread = QThread()

        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        raise NotImplementedError()

    def _routine(self):
        raise NotImplementedError()

    def _init_prober_signals(self):
        '''
            Connect the signals and disable that a new log is printed (in order to prevent double occuring lines
        '''
        self.prober.signals.log_debug.connect(lambda title, desc, details: self._write_debug(desc, print_log=False))
        self.prober.signals.log_info.connect(lambda title, desc, details: self._write_info(desc, print_log=False))
        self.prober.signals.log_warning.connect(lambda title, desc, details: self._write_warning(desc, print_log=False))
        self.prober.signals.log_error.connect(
            lambda title, desc, details: self._write_error(title, desc, details, print_log=False))

    def _write_debug(self, *msg, print_log=True, **kwargs):
        if print_log:
            self.logger.debug(*msg)
        self.signals.write_log.emit("debug", *msg)

    def _write_info(self, *msg, print_log=True, **kwargs):
        if print_log:
            self.logger.info(*msg)
        self.signals.write_log.emit("info", *msg)

    def _write_warning(self, title, msg, desc, err=None, tb=None, print_log=True, *args, **kwargs):
        if err is None and tb is None:
            logmsg_short = f"{desc}."
            logmsg_full = f"{logmsg_short}"
        else:
            logmsg_short = f"{desc}: {err}."
            logmsg_traceback = f"=== TRACEBACK ===\n{tb.format_exc()}"
            logmsg_full = f"{logmsg_short}\n\n{logmsg_traceback}"
        if print_log:
            self.logger.warning(logmsg_full)
        self.signals.warning.emit((title, logmsg_short, logmsg_full))

    def _write_error(self, title, desc, e=None, tb=None, print_log=True, *args, **kwargs):
        if e is None and tb is None:
            logmsg_short = f"{desc}."
            logmsg_full = f"{logmsg_short}"
        else:
            logmsg_short = f"{desc}: {e}."
            logmsg_traceback = f"=== TRACEBACK ===\n{tb.format_exc()}"
            logmsg_full = f"{logmsg_short}\n\n{logmsg_traceback}"
            if print_log:
                self.logger.error(logmsg_full)
            self.signals.error.emit((title, logmsg_short, logmsg_full))

    def write_log(self, msg_type, *args, **kwargs):
        if msg_type == "debug":
            self.logger.debug(*args)
        elif msg_type == "warning":
            self.logger.warning(*args)
        elif msg_type == "error":
            self.logger.error(*args)
        elif msg_type == "fatal":
            self.logger.fatal(*args)
        else:
            self.logger.info(*args)

        self.signals.write_log.emit(msg_type, *args)

    def register_step(*args, **kwargs):
        step_name = "Step"
        if 'step_name' in kwargs:
            step_name = kwargs['step_name']

        def inner(func):
            '''
               do operations with func
            '''
            print(f"Registering step for function {func} - {step_name}")
            return func

        return inner  # this is the fun_obj mentioned in the above content

