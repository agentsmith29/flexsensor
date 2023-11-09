from PySide6.QtWidgets import QLineEdit, QPushButton
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QSlider, QComboBox)
from PySide6.QtCore import Qt, Signal

from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData

import pyqtgraph as pg

from MeasurementEvaluationTool.view.widgets.MeasuredDataInformationWidget import MeasuredDataInformationWidget


class ParameterAdjustmentWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._current_measurement = None
        self._measured_data_list = None

        self.setWindowTitle("Find Peaks Demo")

        layout = QVBoxLayout()
        self.measurement_selection = QComboBox()
        layout.addWidget(self.measurement_selection)

        self._find_peaks_wdg = ParameterAdjustmentWidget()
        self._find_peaks_wdg.apply_fp_param_to_all_clicked.connect(self._on_apply_to_all)

        layout.addWidget(self._find_peaks_wdg)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    @property
    def current_measurement(self):
        return self._current_measurement

    @current_measurement.setter
    def current_measurement(self, value):
        self._current_measurement = value
        self._find_peaks_wdg.measured_data = self.current_measurement

    @property
    def measured_data_list(self):
        return self._measured_data_list

    @measured_data_list.setter
    def measured_data_list(self, value):
        self._measured_data_list = value
        self.current_measurement = self._measured_data_list[0]
        for i, md in enumerate(self._measured_data_list):
            self.measurement_selection.addItem(str(md))
        self.measurement_selection.currentIndexChanged.connect(self._on_measurement_changed)

    def _on_apply_to_all(self, prominence, distance):
        for md in self._measured_data_list:
            md.measurement_properties.find_peaks.set_properties(prominence,distance,None)

    def _on_measurement_changed(self, index):
        self.current_measurement = self._measured_data_list[index]


class ParameterAdjustmentWidget(QWidget):
    apply_fp_param_to_all_clicked = Signal(float, float)

    def __init__(self):
        super().__init__()
        self._measured_data: SingleMeasuredData = None
        # Create the numpy array
        self._init_ui()

    @property
    def measured_data(self):
        return self._measured_data

    @measured_data.setter
    def measured_data(self, value):
        self._measured_data = value
        self.x = self._measured_data.tables.get('_measured_data')['wavelength']
        self.y = self._measured_data.tables.get('_measured_data')['amplitude']
        self.prom_slider.setValue(
            self._measured_data.measurement_properties.find_peaks.prominence * 100)
        self.dist_slider.setValue(
            int(self._measured_data.measurement_properties.find_peaks.distance/10))

        self.dist_slider.setRange(1, len(self.x))
        self.update_plot()

    def _init_ui(self):
        # Create the plot widget
        self.plot_widget = pg.PlotWidget()

        # Create the sliders
        self.prom_slider = QSlider(Qt.Horizontal)
        self.prom_slider.setRange(0, 100)
        #
        self.prom_slider.setTickInterval(5)
        self.prom_slider.setTickPosition(QSlider.TicksBelow)
        self.prom_slider.sliderMoved.connect(self.update_plot)
        self.edit_prom = QLineEdit(str(self.prom_slider.value()))

        self.dist_slider = QSlider(Qt.Horizontal)

        #
        self.dist_slider.setTickInterval(100)
        self.dist_slider.setTickPosition(QSlider.TicksBelow)
        self.dist_slider.sliderMoved.connect(self.update_plot)
        self.edit_dist = QLineEdit(str(self.dist_slider.value()))

        self.btn_apply_to_all = QPushButton('Apply to all')
        self.btn_apply_to_all.clicked.connect(
            lambda: self.apply_fp_param_to_all_clicked.emit(
                self.prom_slider.value() / 100,
                self.dist_slider.value()
            )
        )
        # Create the layout
        prom_layout = QHBoxLayout()
        prom_layout.addWidget(QLabel("Prominence:"))
        prom_layout.addWidget(self.prom_slider)
        prom_layout.addWidget(self.edit_prom)

        dist_layout = QHBoxLayout()
        dist_layout.addWidget(QLabel("Distance:"))
        dist_layout.addWidget(self.dist_slider)
        dist_layout.addWidget(self.edit_dist)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.wdg_measured_information = MeasuredDataInformationWidget(self._measured_data)
        layout.addWidget(self.wdg_measured_information)
        layout.addLayout(prom_layout)
        layout.addLayout(dist_layout)
        layout.addWidget(self.btn_apply_to_all)
        self.setLayout(layout)

    def update_plot(self):
        # Update the prominence and distance values
        prom = self.prom_slider.value() / 100
        dist = self.dist_slider.value()
        self.wdg_measured_information.measurement_data = self.measured_data
        # Update the peaks
        self._measured_data.measurement_properties.find_peaks.prominence = prom
        self._measured_data.measurement_properties.find_peaks.distance = dist

        peaks_wl = self._measured_data.tables.get('_peaks')['wavelength'].compute()
        peaks_amplitude = self._measured_data.tables.get('_peaks')['amplitude'].compute()
        self.edit_dist.setText(str(dist))
        self.edit_prom.setText(str(prom))

        self.plot_widget.clear()
        x = self.x.compute()
        y = self.y.compute()
        self.plot_widget.plot(x.to_list(), y.to_list())
        self.plot_widget.plot(peaks_wl.to_list(), peaks_amplitude.to_list(), pen=None, symbol="o")


if __name__ == "__main__":
    app = QApplication([])

    mypath = r'E:\measurements_06032022\measurements_06032022\mea_mzi2_2_2022_03_06\T40741W177G0\MaskARY1_Jakob\measurement_small'
    mm_data = MeasurementDataLoader.from_folder(mypath)
    # matfile = mm_data.get_measurement(repetition=1, structure_name='mzi2-2')
    matfiles = mm_data.get_measurement_series(structure_name='mzi2-2')
    # matfile = SingleMeasuredData.from_mat(Path(f"{mypath}\measurement_die_22_struct_mzi2_2_20220306_1908_rep_2.mat"))
    window = ParameterAdjustmentWindow(matfiles)
    window.show()
    app.exec_()
