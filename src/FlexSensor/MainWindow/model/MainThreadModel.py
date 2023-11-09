from PySide6.QtCore import QObject, Signal

import Laser as Laser
import AD2CaptDevice as AD2Dev
import Prober as Prober
import MeasurementEvaluationTool as met
import ConfigHandler as Config
from MeasurementRoutines.MeasurementRoutine import MeasurementRoutine


class MainThreadSignals(QObject):
    # Signals for the main thread
    vaut_config_changed = Signal(Config.VAutomatorConfig)
    laser_changed = Signal(Laser.Model, Laser.Controller, Laser.ControlWindow)
    ad2_changed = Signal(AD2Dev.Model, AD2Dev.Controller, AD2Dev.ControlWindow)
    prober_changed = Signal(Prober.Model, Prober.Controller, Prober.ControlWindow)

    measurement_routine_changed = Signal(MeasurementRoutine)

class MainThreadModel(QObject):

    def __init__(self, vaut_config: Config.VAutomatorConfig):
        super().__init__()

        self.signals = MainThreadSignals()

        self._vaut_config: Config.VAutomatorConfig = vaut_config

        self._measurement_routine: MeasurementRoutine = None



        self._ad2_model: AD2Dev.Model = AD2Dev.Model(self.vaut_config.ad2_device_config)
        self._ad2_controller: AD2Dev.Controller = AD2Dev.Controller(
            self._ad2_model)
        self._ad2_window: AD2Dev.ControlWindow = AD2Dev.ControlWindow(
            self._ad2_model, self._ad2_controller)

        # Devices
        self._laser_model: Laser.Model = Laser.Model(self.vaut_config.laser_config)
        self._laser_controller: Laser.Controller = Laser.Controller(self._laser_model, self._ad2_controller)

        self._laser_window: Laser.ControlWindow = Laser.ControlWindow(
            self._laser_model,
            self._laser_controller)

        self._prober_model: Prober.Model = Prober.Model()
        self._prober_controller: Prober.Controller = Prober.Controller(
            self._prober_model,
            self.vaut_config)
        self._prober_window: Prober.ControlWindow = Prober.ControlWindow(
            self._prober_model,
            self._prober_controller)

        # Widgets
        self.mea_eval_tool_model: met.Model  = met.Model()
        self.mea_eval_tool_controller: met.Controller = met.Controller(
            self.mea_eval_tool_model)
        self.mea_eval_tool_window: met.View = met.View(
            self.mea_eval_tool_model,
            self.mea_eval_tool_controller)

    # Implement all getter and setter methods for the model here
    @property
    def vaut_config(self) -> Config.VAutomatorConfig:
        return self._vaut_config

    @vaut_config.setter
    def vaut_config(self, value: Config.VAutomatorConfig):
        self._vaut_config = value
        self.signals.vaut_config_changed.emit(self.vaut_config)

    @property
    def laser_model(self) -> Laser.Model:
        return self._laser_model

    @laser_model.setter
    def laser_model(self, value: Laser.Model):
        self._laser_model = value
        self.signals.laser_changed.emit(self.laser_model, self.laser_controller, self.laser_window)


    @property
    def laser_controller(self) -> Laser.Controller:
        return self._laser_controller

    @laser_controller.setter
    def laser_controller(self, value: Laser.Controller):
        self._laser_controller = value
        self.signals.laser_changed.emit(self.laser_model, self.laser_controller, self.laser_window)

    @property
    def laser_window(self) -> Laser.ControlWindow:
        return self._laser_window

    @laser_window.setter
    def laser_window(self, value: Laser.ControlWindow):
        self._laser_window = value
        self.signals.laser_changed.emit(self.laser_model, self.laser_controller, self.laser_window)


    @property
    def ad2_model(self) -> AD2Dev.Model:
        return self._ad2_model

    @ad2_model.setter
    def ad2_model(self, value: AD2Dev.Model):
        self._ad2_model = value
        self.signals.ad2_changed.emit(self.ad2_model, self.ad2_controller, self.ad2_window)

    @property
    def ad2_controller(self) -> AD2Dev.Controller:
        return self._ad2_controller

    @ad2_controller.setter
    def ad2_controller(self, value: AD2Dev.Controller):
        self._ad2_controller = value
        self.signals.ad2_changed.emit(self.ad2_model, self.ad2_controller, self.ad2_window)

    @property
    def ad2_window(self) -> AD2Dev.ControlWindow:
        return self._ad2_window

    @ad2_window.setter
    def ad2_window(self, value: AD2Dev.ControlWindow):
        self._ad2_window = value
        self.signals.ad2_changed.emit(self.ad2_model, self.ad2_controller, self.ad2_window)

    @property
    def prober_model(self) -> Prober.Model:
        return self._prober_model

    @prober_model.setter
    def prober_model(self, value: Prober.Model):
        self._prober_model = value
        self.signals.prober_changed.emit(self.prober_model, self.prober_controller, self.prober_window)

    @property
    def prober_controller(self) -> Prober.Controller:
        return self._prober_controller

    @prober_controller.setter
    def prober_controller(self, value: Prober.Controller):
        self._prober_controller = value
        self.signals.prober_changed.emit(self.prober_model, self.prober_controller, self.prober_window)

    @property
    def prober_window(self) -> Prober.ControlWindow:
        return self._prober_window

    @prober_window.setter
    def prober_window(self, value: Prober.ControlWindow):
        self._prober_window = value
        self.signals.prober_changed.emit(self.prober_model, self.prober_controller, self.prober_window)


    @property
    def measurement_routine(self) -> MeasurementRoutine:
        return self._measurement_routine

    @measurement_routine.setter
    def measurement_routine(self, value: MeasurementRoutine):
        self._measurement_routine = value
        self.signals.measurement_routine_changed.emit(self.measurement_routine)






