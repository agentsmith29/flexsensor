import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from MeasurementData.MeasuredData.MeasuredData import MeasuredData


class MeasuredDataInformationWidget(QGroupBox):
    def __init__(self, measured_data: MeasuredData):
        super().__init__()

        self._wafer_number = "unknown"
        self._die_number = "unknown"
        self._structure_name = "unknown"
        self._repetition = "unknown"
        self._timestamp = "unknown"
        self._measurement_time = 0
        self._init_ui()
        self.measurement_data = measured_data

    def _init_ui(self):
        # Create QLabel widgets to display the information
        layout = QGridLayout()
        self.wafer_label = QLabel()
        self.die_label = QLabel()
        self.structure_label = QLabel()
        layout.addWidget(self.wafer_label, 0, 0)
        layout.addWidget(self.die_label, 0, 1)
        layout.addWidget(self.structure_label, 0, 2)

        self.repetition_label = QLabel()
        self.timestamp_label = QLabel()
        self.measurement_time_label = QLabel()
        layout.addWidget(self.repetition_label, 1, 0)
        layout.addWidget(self.timestamp_label, 1, 1)
        layout.addWidget(self.measurement_time_label, 1, 2)

        # Create a vertical layout to arrange the QLabel widgets

        # Set the layout for the group box
        self.setLayout(layout)

    @property
    def measurement_data(self):
        return self._measurement_data

    @measurement_data.setter
    def measurement_data(self, value):
        if value is not None:
            self._measurement_data = value
            self._wafer_number = self._measurement_data.wafer_properties.wafer_number
            self._die_number = self._measurement_data.wafer_properties.die_number
            self._structure_name = self._measurement_data.wafer_properties.structure_name
            self._repetition = self._measurement_data.wafer_properties.repetition
            self._timestamp = "none"
            self._measurement_time = self._measurement_data.ad2_properties.measurement_time

        self.wafer_label.setText(f'Wafer Number: {self._wafer_number}')
        self.die_label.setText(f'Die Number: {self._die_number}')
        self.structure_label.setText(f'Structure Name: {self._structure_name}')
        self.repetition_label.setText(f'Repetition: {self._repetition}')
        self.timestamp_label.setText(f'Timestamp: {self._timestamp}')
        self.measurement_time_label.setText(f'Measurement Time: {np.round(self._measurement_time, 3)}')

