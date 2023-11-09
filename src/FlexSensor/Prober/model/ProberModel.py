from pathlib import Path

from PySide6.QtCore import QObject, Signal

from MeasurementData.Properties.WaferProperties import WaferProperties


class ProberSignals(QObject):
    '''
      Defines the signals available from a running prober thread.
      The signals are always constructed for proagating it's status
      to a Message Bix with
      Signal(title, description, details)
      '''

    connected_changed = Signal(bool)
    version_changed = Signal(str)
    wafer_map_changed = Signal(Path)

    die_changed = Signal(int)
    curr_die_row_changed = Signal(int)
    curr_die_col_changed = Signal(int)

    chuck_x_changed = Signal(float)
    chuck_z_changed = Signal(float)
    chuck_y_changed = Signal(float)

    errors_changed = Signal(list)
    warnings_changed = Signal(list)




    log_debug = Signal(str, str, str)
    log_info = Signal(str, str, str)
    log_warning = Signal(str, str, str)
    log_error = Signal(str, str, str)


class ProberModel:

    def __init__(self):
        self.signals = ProberSignals()

        self._connected: bool = False
        self._version: str = "Unknown Version"

        self._die: int = 0
        self._die_row: int = 0
        self._die_col: int = 0

        self._chuck_x: float = 0
        self._chuck_y: float = 0
        self._chuck_z: float = 0

        self._errors: list = []
        self._warnings: list = []

        self._wafer_map = None

    @property
    def laser_properties(self) -> WaferProperties:
        return WaferProperties(self.acceleration,
                               self.deceleration,
                               self.velocity,
                               (self.sweep_start_wavelength, self.sweep_stop_wavelength))
    @property
    def connected(self) -> bool:
        return self._connected

    @connected.setter
    def connected(self, value: bool):
        self._connected = value
        self.signals.connected_changed.emit(value)

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value
        self.signals.version_changed.emit(value)

    @property
    def wafer_map(self) -> Path:
        return self._wafer_map

    @wafer_map.setter
    def wafer_map(self, value: Path):
        self._wafer_map = value
        self.signals.wafer_map_changed.emit(value)

    @property
    def die(self) -> int:
        return self._die

    @die.setter
    def die(self, value: int):
        self._die = value
        self.signals.die_changed.emit(value)

    @property
    def die_row(self) -> int:
        return self._die_row

    @die_row.setter
    def die_row(self, value: int):
        self._die_row = value
        self.signals.curr_die_row_changed.emit(value)

    @property
    def die_col(self) -> int:
        return self._die_col

    @die_col.setter
    def die_col(self, value: int):
        self._die_col = value
        self.signals.curr_die_col_changed.emit(value)

    @property
    def chuck_x(self) -> float:
        return self._chuck_x

    @chuck_x.setter
    def chuck_x(self, value: float):
        self._chuck_x = float(value)
        self.signals.chuck_x_changed.emit(self._chuck_x)

    @property
    def chuck_y(self) -> float:
        return self._chuck_y

    @chuck_y.setter
    def chuck_y(self, value: float):
        self._chuck_y = float(value)
        self.signals.chuck_y_changed.emit(self._chuck_y)

    @property
    def chuck_z(self) -> float:
        return self._chuck_z

    @chuck_z.setter
    def chuck_z(self, value: float):
        self._chuck_z = float(value)
        self.signals.chuck_z_changed.emit(self.chuck_z)

    @property
    def errors(self) -> list:
        return self._errors

    @errors.setter
    def errors(self, value: list):
        self._errors = value
        self.signals.errors_changed.emit(value)

    @property
    def warnings(self) -> list:
        return self._warnings

    @warnings.setter
    def warnings(self, value: list):
        self._warnings = value
        self.signals.warnings_changed.emit(value)
