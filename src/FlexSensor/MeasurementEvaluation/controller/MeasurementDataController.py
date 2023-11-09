import logging

from MeasurementData.MeasuredData.MeasuredData import MeasuredData
from MeasurementData.MeasuredData.MultiMeasuredData import MultiMeasuredData
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
from MeasurementData.MeasuredData.SupportClasses.MeasurementDataLoader import MeasurementDataLoader
from MeasurementEvaluation.model.MeasurementDataModel import MeasurementDataModel


class MeasurementDataController:

    def __init__(self, model: MeasurementDataModel, path):
        self.logger = logging.getLogger("MeasurementDataController")
        self._model = model

        self._model.path = path
        self._md_loader = MeasurementDataLoader.from_folder(self._model.path)

        self._model.selected_measurements = []
        self._model.measurement_list = self._md_loader.sorted_files


    @property
    def consolidated_measurements(self):
        return self._consolidated_measurements

    @consolidated_measurements.setter
    def consolidated_measurements(self, value):
        self._consolidated_measurements = value

    @property
    def all_measurements(self):
        return self._model.measurement_list

    @property
    def list_of_measurements(self) -> list[SingleMeasuredData]:
        return self._model.selected_measurements

    @property
    def selected_measurement(self) -> SingleMeasuredData:
        return self._model.display_measurement

    def select_measurement(self, selected_measurement: MeasuredData):
        self._model.display_measurement = selected_measurement

    def consolidate_measurements(self, measurement_selection):
        self._model.consolidated_measurement = MultiMeasuredData(measurement_selection)
        self._model.selected_measurements = measurement_selection
        self.select_measurement(self._model.consolidated_measurement)

    def recalculate_measurements(self, measurement_selection):
        self.logger.info("Recalculating all measurements")
        for md in measurement_selection:
            md.calulate_all()

    def load_from_folder(self):
        raise NotImplementedError

    def add_measurement(self):
        pass