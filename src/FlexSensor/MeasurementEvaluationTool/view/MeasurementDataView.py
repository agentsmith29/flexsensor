import sys

import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QTableView, \
    QComboBox, QPushButton, QGridLayout

import MeasurementData
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
from MeasurementEvaluationTool.controller.MeasurementDataController import MeasurementDataController
from MeasurementEvaluationTool.model.MeasurementDataModel import MeasurementDataModel
from generics.PandasTableModel import PandasTableModel
from MeasurementEvaluationTool.view.ParameterAdjustmentView import ParameterAdjustmentWindow
from MeasurementEvaluationTool.view.widgets.MeasurementSelectionWidget import MeasurementSelectionWidget
from MeasurementEvaluationTool.view.widgets.PlotViewWidget import PlotViewWidget
from generics.logger import setup_logging


class MeasurementDataView(QWidget):
    def __init__(self, model: MeasurementDataModel, controller: MeasurementDataController):
        super().__init__()
        self._model = model
        self._controller = controller
        self.layout = QGridLayout()

        self._model.signals.selected_measurement_changed.connect(self._on_selected_measurement_changed)

        self._init_ui()

    def _init_ui(self):
        self.find_peaks_view = ParameterAdjustmentWindow()

        # Add a view for selecting the measurement
        self.measurement_selection = MeasurementSelectionWidget(self._controller.all_measurements)

        self.measurement_selection.signals.open_find_peaks_window.connect(self._on_adapt_parameters_clicked)
        self.measurement_selection.signals.on_consolidate_measurement_clicked.connect(self._on_consolidate_clicked)
        self.measurement_selection.signals.on_recalculation_clicked.connect(self._on_recalculate_clicked)
        self.measurement_selection.signals.on_show_item_click.connect(self._on_show_item_clicked)

        # self.measurement_selection.selection.selected_data_changed.connect(self._on_selection_changed)
        self.layout.addWidget(self.measurement_selection, 0, 0, 2, 1)

        self.plot_widget = PlotViewWidget()  # pg.PlotWidget()
        self.layout.addWidget(self.plot_widget, 0, 1, 1, 1)

        # Display the data in an QTableWidget
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view, 1, 1, 1, 1)

        # Add a dropdown
        self.btn_consolidate = QPushButton('Consolidate all')
        self.btn_consolidate.clicked.connect(self._on_consolidate_clicked)
        self.layout.addWidget(self.btn_consolidate, 2, 0, 1, 1)

        self.dd_select_measurement_table = QComboBox()
        self.dd_select_measurement_table.currentIndexChanged.connect(self._on_data_table_changed)
        self.layout.addWidget(self.dd_select_measurement_table, 2, 1, 1, 1)

        self.setLayout(self.layout)
        # self._controller.select_measurement(0)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _on_show_item_clicked(self, measurement_selection: SingleMeasuredData):
        measurement_selection.calulate_all()
        self._controller.select_measurement(measurement_selection)

    def _on_consolidate_clicked(self, measurement_selection):
        self._controller.recalculate_measurements(measurement_selection)
        self._controller.consolidate_measurements(measurement_selection)
        # self._current_measurement = self._controller.consolidated_measurements

    def _on_recalculate_clicked(self, measurement_selection):
        self._controller.recalculate_measurements(measurement_selection)

    def _on_adapt_parameters_clicked(self, measurement_selection):
        self.find_peaks_view.measured_data_list = measurement_selection
        self.find_peaks_view.show()

    def _on_selection_changed(self, it: int):
        # self._controller.select_measurement(it)
        self.measurement_selection.set_selected_data(self._controller.selected_measurement)

    def _on_data_table_changed(self, idx):
        table_name = self.dd_select_measurement_table.itemData(idx)
        print(f"{table_name} - {type(table_name)}")
        # print(self._current_measurement.tables.get(table_name))
        table = self._controller.selected_measurement.tables.get(table_name)
        # Define plt function here
        self.table_view_model = PandasTableModel(table)
        self.table_view.setModel(self.table_view_model)

        # This will be removed later and is only for quick and dirty hardcoded plotting
        if table_name == "_measured_data":
            pass
        #    self._plot_measurement_table(table_name)
        elif table_name == "_wg_param":
            self._controller.selected_measurement.tables.get_plot_function('ng (FSR)')(self.plot_widget)

            #self._plot_ng_table(table_name)

    def _on_selected_measurement_changed(self, measurement: MeasurementData):
        self._current_measurement = measurement
        # Populate the measurement ment selection
        self.dd_select_measurement_table.clear()
        for table in measurement.tables.to_list():
            # id in table -> table[2] = 'Friendly name', table[1] = 'table name'
            self.dd_select_measurement_table.addItem(table[2], table[1])
        #self.dd_select_measurement_table.addItem( measurement.tables.to_list()[2][2], table[2][1])

    # ==================================================================================================================
    #
    # =============================================================================================================
    def _plot_measurement_table(self, table_name, x_axis="wavelength", y_axis="detrend"):
        self.plot_widget.ax.clear()
        data = self._controller.selected_measurement.tables.get(table_name)
        self.plot_widget.ax.plot(data[x_axis], data[y_axis], 'b-')[0]
        self.plot_widget.ax.set_xlim(np.min(data[x_axis]), np.max(data[x_axis]))
        self.plot_widget.ax.set_ylim(np.min(data[y_axis]), np.max(data[y_axis]))
        # Scatter plot of the peaks
        df_peaks = self._current_measurement.peaks
        self.plot_widget.ax.scatter(df_peaks[x_axis], df_peaks[y_axis], marker='x', color='red')
        self.plot_widget.ax.set_xlabel('Wavelength [nm]')
        self.plot_widget.ax.set_ylabel('Amplitude [1]')
        self.plot_widget.ax.set_title('Measured data')
        self.plot_widget.ax.grid(True)
        self.plot_widget.ax.legend([y_axis, 'Peaks'])

        self.plot_widget.canvas.draw()

    def _plot_ng_table(self, table_name, x_axis="lambda", y_axis="FSR"):
        self.plot_widget.ax.clear()
        data = self._controller.selected_measurement.tables.get(table_name)
        self.plot_widget.ax.plot(data[x_axis], data[y_axis])
        self.plot_widget.ax.set_xlim(np.min(data[x_axis]), np.max(data[x_axis]))
        self.plot_widget.ax.set_ylim(np.min(data[y_axis]), np.max(data[y_axis]))
        # Scatter plot of the peaks
        self.plot_widget.ax.set_xlabel('Wavelength [nm]')
        self.plot_widget.ax.set_ylabel(f'{y_axis} [1]')
        self.plot_widget.ax.grid(True)

        self.plot_widget.canvas.draw()

def convert_mat(mypath):
    #mypath = (r'F:\measurements_06032022')
    md_loader = MeasurementDataLoader.glob_files(mypath, '*.mat')
    #measurement_list = md_loader.sorted_files

    for measurement in md_loader:
        SingleMeasuredData.convert(measurement)
        print('done')


if __name__ == "__main__":
    app = QApplication()
    setup_logging()

    #mypath = (r'F:\measurements_06032022\measurements_06032022\mea_mzi1_2022_03_06\T40741W177G0')
    #mypath = (r'F:\measurements_06032022')
    #convert_mat(mypath)
    #exit()

    mypath = (r'F:\measurements_v2_06032022')

    model = MeasurementDataModel()
    controller = MeasurementDataController(model, mypath)
    window = MeasurementDataView(model, controller)
    window.show()

    sys.exit(app.exec())
