import time

import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog
from numpy import ndarray

from MeasurementData.MeasuredData.MeasuredData import MeasuredData
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
import mcpy
from MeasurementData.MeasuredData.SupportClasses.MatplotlibPlottingHelpers import MPLPlottingHelper
from MeasurementData.MeasuredData.SupportClasses.MeasurementDataLoader import MeasurementDataLoader

class MultiMeasuredData(MeasuredData):

    def __init__(self, single_measurements: list[SingleMeasuredData]):
        self._single_measurements = single_measurements

        super().__init__(laser_properties=self._single_measurements[0].laser_properties,
                         ad2_properties=self._single_measurements[0].ad2_properties,
                         wafer_properties=self._single_measurements[0].wafer_properties,
                         waveguide_properties=self._single_measurements[0].waveguide_properties,
                         measurement_properties=self._single_measurements[0].measurement_properties,
                         )
        self.wafer_properties._structure_name += " - Mean"

        self._recalculate_measured_data()
        self.consolidate_measurement()
        self.calculate_mean_and_std()
        self.calculate_wg_params(table='_peaks')
        self.calculate_all(table='_peaks')

    def consolidate_measurement(self):
        self.logger.info("Consolidating all measurements to one measurement")
        progress = QProgressDialog(f"Reading files...", "Abort", 0, len(self._single_measurements))
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        tmp_measured_data = []
        for i, mea, it in QProgressBarWindow(self._single_measurements):
            it.print(f"Consolidating measurement {str(mea)}")
            tmp_measured_data.append(pd.DataFrame(
                mea.tables.get('_peaks')['wavelength'].reset_index()[:].values,
                columns=[f'index_{mea.wafer_properties.repetition}',
                         f'wavelength_{mea.wafer_properties.repetition}']
            ))

        self._measured_data = self._tables.update(pd.concat(tmp_measured_data, axis=1), '_measured_data')

    def _recalculate_measured_data(self):
        self.logger.info("Recalculating all measurements")

        for i, mea, it  in QProgressBarWindow(self._single_measurements):
            mea.calulate_all()

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def calculate_mean_and_std(self):
        self._peaks['wavelength'] = self._measured_data.filter(like='wavelength').apply(
            lambda row: mcpy.DirectObservations(row), axis=1)
        self._peaks['index'] = self._measured_data.filter(like='index').apply(
            lambda row: mcpy.DirectObservations(row), axis=1)
        self._tables.update(self._peaks, '_peaks')

    def calculate_all(self, table='_peaks', N=100000):
        peaks_wl: ndarray = self.tables.get(table)['wavelength'].to_numpy()
        try:
            if len(peaks_wl) % 2 == 1:
                self.logger.warning(f"[{self}] | Number of peaks not even ({len(peaks_wl)}), removing last peak.")
                peaks_wl = peaks_wl[:-1]
            self.logger.info(f"[{self}] | Reshaping {np.shape(peaks_wl)} to (-1, 2)")
            self._wg_param = pd.DataFrame(peaks_wl.reshape(-1, 2), columns=['P1', 'P2'])  # .astype(Uncertainty)

            self._wg_param['P1 (MC)'] = self._wg_param.apply(
                lambda row: row['P1'].rand(N), axis=1)

            self._wg_param['P2 (MC)'] = self._wg_param.apply(
                lambda row: row['P2'].rand(N), axis=1)

            self._wg_param['FSR (MC)'] = self._wg_param.apply(
                lambda row: row['P2 (MC)'] - row['P1 (MC)'], axis=1)

            self._wg_param['lambda (MC)'] = self._wg_param.apply(
                lambda row: (row['P2 (MC)']+row['P1 (MC)'])/2, axis=1)

            self._wg_param['ng (MC)'] = self._wg_param.apply(
                lambda row: self.waveguide_properties.group_index(row['lambda (MC)'], row['FSR (MC)'] ), axis=1)
            # Place here any other calculations

            # Update the _tables
            self._tables.update(self._wg_param, '_wg_param')
            self._tables.add_plot('ng (FSR)',
                                  plot_function=lambda plotwidget: MPLPlottingHelper.plt_errorbar_mcsamples(
                                      plotwidget,
                                      x_values=self._wg_param['lambda (MC)'],
                                      y_values=self._wg_param['ng (MC)']))
            self._tables.add_plot('FSR (FSR)',
                                  plot_function=lambda plotwidget: MPLPlottingHelper.plt_errorbar_mcsamples(
                                      plotwidget,
                                      x_values=self._wg_param['lambda (MC)'],
                                      y_values=self._wg_param['FSR (MC)']))
        except Exception as e:
            print(f"Error {e}")

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def to_dict(self) -> dict:
        return {
            "laser_properties": self._laser_properties.to_dict(),
            "wafer_properties": self._wafer_properties.to_dict(),
            "measurement_properties": self._measurement_properties.to_dict(),
            "waveguide_properties": self._waveguide_properties.to_dict(),
            "amplitudes": [i.to_dict() for i in self._single_measurements],

        }

    def __str__(self):
        return f"{self.wafer_properties.wafer_number}/" \
               f"{self.wafer_properties.die_number}/" \
               f"{self.wafer_properties.structure_name}-Sum"


if __name__ == "__main__":
    setup_logging()

    mypath = 'E:\measurements_06032022\measurements_06032022\mea_mzi2_2_2022_03_06\T40741W177G0\MaskARY1_Jakob\measurement_small'
    mm_data = MeasurementDataLoader.from_folder(mypath)
    print(mm_data.wafers)
    print(mm_data.dies)
    print(mm_data.structure_name)

    filtered_files = mm_data.get_measurement_series(structure_name='mzi2-2')

    data = MultiMeasuredData(filtered_files)
    print(data._wg_param)
    # ädata.generate_mat_file(r'E:\test.mat')
