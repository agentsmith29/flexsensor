from pathlib import Path

from PySide6.QtCore import Signal, QObject

from MeasurementData.MeasuredData.MultiMeasuredData import MultiMeasuredData
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData


class MeasuredDataSignals(QObject):
    path_changed = Signal(Path)

    list_of_measurements_changed = Signal(list)
    all_measurements_changed = Signal(dict)

    num_of_measurements = Signal(int)
    selected_measurement_changed = Signal(SingleMeasuredData)
    consolidated_measurements_changed = Signal(MultiMeasuredData)


class MeasurementDataModel:
    def __init__(self):
        self.signals = MeasuredDataSignals()

        self._path: Path = None
        self._measurement_list: dict[str, dict[int, dict[str, list[SingleMeasuredData]]]] = None

        self._consolidated_measurement: MultiMeasuredData = None
        self._display_measurement: SingleMeasuredData = None
        self._selected_measurements: list[SingleMeasuredData] = []

        self._num_of_measurements: int = 0

    @property
    def consolidated_measurement(self):
        return self._consolidated_measurement

    @consolidated_measurement.setter
    def consolidated_measurement(self, value):
        self._consolidated_measurement = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self.signals.path_changed.emit(self.path)

    @property
    def measurement_list(self) -> dict[str, dict[int, dict[str, list[SingleMeasuredData]]]]:
        return self._measurement_list

    @measurement_list.setter
    def measurement_list(self, value: dict[str, dict[int, dict[str, list[SingleMeasuredData]]]]) -> None:
        self._measurement_list = value
        self.signals.all_measurements_changed.emit(self.measurement_list)

    @property
    def selected_measurements(self) -> list[SingleMeasuredData]:
        return self._selected_measurements

    @selected_measurements.setter
    def selected_measurements(self, value: list[SingleMeasuredData]) -> None:
        self._selected_measurements = value
        self.num_of_measurements = len(self.selected_measurements)
        self.signals.list_of_measurements_changed.emit(self.selected_measurements)

    @property
    def num_of_measurements(self) -> int:
        return self._num_of_measurements

    @num_of_measurements.setter
    def num_of_measurements(self, value: list[SingleMeasuredData]) -> None:
        self._num_of_measurements = value
        self.signals.num_of_measurements.emit(self.num_of_measurements)

    @property
    def display_measurement(self) -> SingleMeasuredData:
        return self._display_measurement

    @display_measurement.setter
    def display_measurement(self, value: SingleMeasuredData) -> None:
        self._display_measurement = value
        self.signals.selected_measurement_changed.emit(self.display_measurement)
