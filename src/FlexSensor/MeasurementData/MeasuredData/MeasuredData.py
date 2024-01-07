import logging
import os
from pathlib import Path

import LaserControl
import numpy as np
import pandas as pd
import scipy
from numpy import ndarray

from MeasurementData.Properties.AD2CaptDeviceProperties import AD2CaptDeviceProperties
from MeasurementData.Properties.LaserProperties import LaserProperties
from MeasurementData.MeasuredData.SupportClasses.MeasurementDataTables import MeasurementDataTables
from MeasurementData.Properties.MeasurementProperties import MeasurementProperties, \
    MPropertiesFindPeaks, WaveguideProperties
from MeasurementData.Properties.WaferProperties import WaferProperties


class MeasuredData:


    def __init__(self, laser_properties: LaserProperties, ad2_properties: AD2CaptDeviceProperties,
                 wafer_properties: WaferProperties, waveguide_properties: WaveguideProperties,
                 measurement_properties: MeasurementProperties):
        #super().__init__()
        self.logger = logging.getLogger("MeasuredSignal")
        # ==============================================================================================================
        # Tables
        self._tables: MeasurementDataTables = MeasurementDataTables()

        # ==============================================================================================================
        # Properties for storing information
        #self._laser_properties: LaserProperties = laser_properties  # Laser Properties
        #self._ad2_properties: AD2CaptDeviceProperties = ad2_properties  # AD2CaptDev Properties
        #self._wafer_properties: WaferProperties = wafer_properties  # Wafer Properties
        #self._waveguide_properties: WaveguideProperties = waveguide_properties  # Waveguide Properties
        # Measurement properties like findpeaks parameter
        #self._measurement_properties: MeasurementProperties = MeasurementProperties(
        #    MPropertiesFindPeaks(0.1, 10000, None))

        # ==============================================================================================================
        # Dataframe with measured values
        self._measured_data: pd.DataFrame = self._tables.append(pd.DataFrame(), '_measured_data', "Measured Data")
        # Calculation Tables
        # Stores the found peaks
        self._peaks: pd.DataFrame = self._tables.append(pd.DataFrame(), '_peaks', 'Peaks')
        # Store wg parameters like FSR, and ng
        self._wg_param: pd.DataFrame = self._tables.append(pd.DataFrame(), '_wg_param', 'Waveguide Parameters')

        # ==============================================================================================================
        # COnnect the signals
        self.measurement_properties.find_peaks.properties_changed.connect(self.find_peaks)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    @property
    def waveguide_properties(self):
        return self._waveguide_properties

    @waveguide_properties.setter
    def waveguide_properties(self, value):
        self._waveguide_properties = value

    @property
    def measurement_properties(self):
        return self._measurement_properties

    @measurement_properties.setter
    def measurement_properties(self, value):
        self._measurement_properties = value

    @property
    def ad2_properties(self):
        return self._ad2_properties

    @ad2_properties.setter
    def ad2_properties(self, value):
        self._ad2_properties = value

    @property
    def laser_properties(self):
        return self._laser_properties

    @laser_properties.setter
    def laser_properties(self, value):
        self._laser_properties = value

    @property
    def wafer_properties(self):
        return self._wafer_properties

    @wafer_properties.setter
    def wafer_properties(self, value):
        self._wafer_properties = value

    # ==================================================================================================================
    # Properties
    # ==================================================================================================================
    @property
    def tables(self) -> MeasurementDataTables:
        return self._tables

    @property
    def peaks(self) -> pd.DataFrame:
        return self._peaks

    # ==================================================================================================================
    # Calculations and table creations
    # ==================================================================================================================
    def calculate_wg_params(self, table="_peaks"):
        peaks_wl: ndarray = self.tables.get(table)['wavelength'].to_numpy()
        try:
            if len(peaks_wl) % 2 == 1:
                self.logger.warning(f"[{self}] | Number of peaks not even ({len(peaks_wl)}), removing last peak.")
                peaks_wl = peaks_wl[:-1]
            self.logger.info(f"[{self}] | Reshaping {np.shape(peaks_wl)} to (-1, 2)")
            self._wg_param = pd.DataFrame(peaks_wl.reshape(-1, 2), columns=['P1', 'P2'])
            self._wg_param['FSR'] = self._wg_param.apply(lambda row: row['P2'] - row['P1'], axis=1)
            self._wg_param['lambda'] = self._wg_param.apply(lambda row: np.mean((row['P2'], row['P1'])), axis=1)
            self._wg_param['ng'] = self.waveguide_properties.group_index(self._wg_param)
            # self._wg_param.apply(lambda row: (row['lambda'] ** 2) / (row['FSR'] * dl), axis=1)
            # Filter outliers
            self._wg_param = self._tables.update(self._wg_param[(np.abs(scipy.stats.zscore(self._wg_param['ng'])) < 2)],
                                                 '_wg_param')
        except Exception as e:
            print(f"Error {e}")

    def __str__(self):
        return f"{self.wafer_properties.wafer_number}/" \
               f"{self.wafer_properties.die_number}/" \
               f"{self.wafer_properties.structure_name} - {self.wafer_properties.repetition}"

    # ==================================================================================================================
    # I/O - Operations and Plotting
    # ==================================================================================================================
    def _save_mat_file(self, filename: str) -> object:

        self._mat_filename = Path(filename)
        dirname = self._mat_filename.parent.absolute()
        self.logger.info(f"[{self}] | Generating mat file and saving to {self._mat_filename.name} (folder: {dirname})")
        if self._mat_filename is None or self._mat_filename == "":
            raise ValueError("No mat file generated. Filename is not defined")

        if not str(self._mat_filename).endswith(".mat"):
            raise ValueError("No mat file generated. Filename does not end with .mat")
        if self._measured_data is None:
            raise ValueError(
                "No mat file generated. No measured amplitude data. No mat file produced fot this structure.")
        # Get the file name from file

        # Make a path
        # Check if path exists
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as exc:  # Guard against
                raise ValueError("No mat file generated. Could not create directory")
        mdic = self.to_dict()
        #print(mdic)
        scipy.io.savemat(self._mat_filename, mdict=mdic)
        #self._measured_data.to_csv(self.datafile)
        self.write_matlab_file(self._mat_filename, self.datafile, f"{self._mat_filename.parent}/load_all.m")

        self.logger.info(f"[{self}] | Stored matlab file to {self._mat_filename}")

        return self._mat_filename

    def write_matlab_file(self, mat_file, csv_file, filename: str) -> object:
        mfile = ""
        mfile += "load('" + str(filename) + "');"
        # load csv with matlab
        mfile += "data = readcsv('" + str(self.datafile) + "');"
        # save matlab file
        with open(filename, 'w') as f:
            f.write(mfile)

    # ==================================================================================================================
    # abstract methods
    # ==================================================================================================================
    def find_peaks(self):
        raise NotImplementedError()

    def to_dict(self) -> dict:
        raise NotImplementedError()
