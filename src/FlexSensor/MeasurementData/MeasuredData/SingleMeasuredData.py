import sys

from FlexSensor.MeasurementData.MeasuredData.MeasuredData import MeasuredData
from FlexSensor.generics.GenericProperties import GenericProperties

#from examples.Properties.AD2CaptDeviceProperties import AD2CaptDeviceProperties
#from examples.Properties.LaserProperties import LaserProperties
#from examples.Properties.MeasurementProperties import WaveguideProperties, MeasurementProperties
#from examples.Properties.WaferProperties import WaferProperties

sys.path.append("../flexsensorpy")
sys.path.append("../mcpy")
import pathlib
from datetime import datetime


import scipy.io
import numpy as np
import pandas as pd

import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from numpy import linspace
from scipy import signal
from scipy.io import matlab
from scipy.signal import find_peaks
import scipy

import mcpy




class SingleMeasuredData(MeasuredData):

    # ==================================================================================================================
    # Load a Measurement data from a matlab mat-file
    # ==================================================================================================================
    # @classmethod
    # def from_mat(cls, mat_file: Path | str) -> 'SingleMeasuredData':
    #     """
    #     This allows to open "old" mat files, that do not have some data.
    #     """
    #     mat_file = pathlib.Path(mat_file)
    #     logging.info(f"Loading {mat_file.name}")
    #     matf = scipy.io.loadmat(mat_file)
    #
    #     inst = cls(
    #         laser_properties=
    #         #LaserProperties(
    #         #    mcpy.Rectangular(2, 0.01, unit='nm/s'),
    #         #   mcpy.Rectangular(2, 0.01, unit='nm/s'),
    #         #    mcpy.Rectangular(0.5, 0.01, unit='nm/s^2'),
    #         #    (mcpy.Rectangular(835, 0.01, unit='nm'), mcpy.Rectangular(870, 0.01, unit='nm'))
    #         #),
    #         ad2_properties=AD2CaptDeviceProperties(
    #             0, 0, matf['ad2_sample_rate'], matf['ad2_total_samples'], matf['measure_time']
    #         ),
    #         wafer_properties=WaferProperties(
    #             matf['wafer_nr'],
    #             matf['structure_name'],
    #             matf['die_nr'],
    #             matf['chuck_col'],
    #             matf['chuck_row'],
    #             (int(matf['structure_x_in']), int(matf['structure_y_in'])),
    #             (int(matf['structure_x_out']), int(matf['structure_y_out'])),
    #             int(mat_file.name.split('_')[9].replace('.mat', ''))
    #         ),
    #         waveguide_properties=WaveguidePropertiesMZI(
    #             length1=mcpy.Rectangular(10e6, 20, unit='nm'),
    #             length2=mcpy.Rectangular(10.38e6, 20, unit='nm'),
    #             width=mcpy.Rectangular(550, 20, unit='nm'),
    #             height=mcpy.Rectangular(625, 2.405, unit='nm')),
    #         measurement_properties=MeasurementProperties(
    #             MPropertiesFindPeaks(0.1, 10000, None)
    #         ),
    #         timestamp=matf['timestamp'],
    #         measurement_file=None,
    #         measurement_data=matf['amplitude'][0]
    #     )
    #     """
    #     date_format = '%a %b %d %H:%M:%S %Y'
    #     x = datetime. strptime(
    #     re.search('(?<=Created on: ).*', matf['__header__'].decode('UTF-8')).group(0),
    #     date_format)"""
    #
    #     return inst
    #
    # @classmethod
    # def from_mat_v2(cls, mat_file: Path | str):
    #     def loadmat(filename):
    #         '''
    #         this function should be called instead of direct spio.loadmat
    #         as it cures the problem of not properly recovering python dictionaries
    #         from mat files. It calls the function check keys to cure all entries
    #         which are still mat-objects
    #         '''
    #         data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    #         return _check_keys(data)
    #
    #     def _check_keys(dict):
    #         '''
    #         checks if entries in dictionary are mat-objects. If yes
    #         todict is called to change them to nested dictionaries
    #         '''
    #         for key in dict:
    #             if isinstance(dict[key], matlab.mio5_params.mat_struct):
    #                 dict[key] = _todict(dict[key])
    #         return dict
    #
    #     def _todict(matobj):
    #         '''
    #         A recursive function which constructs from matobjects nested dictionaries
    #         '''
    #         dict = {}
    #         for strg in matobj._fieldnames:
    #             elem = matobj.__dict__[strg]
    #             if isinstance(elem, matlab.mio5_params.mat_struct):
    #                 dict[strg] = _todict(elem)
    #             else:
    #                 dict[strg] = elem
    #         return dict
    #
    #     if isinstance(mat_file, str):
    #         mat_file = Path(mat_file)
    #
    #     logging.info(f"Loading {mat_file.name}")
    #     matf = loadmat(mat_file)
    #     # mcpy.Uncertainty.from_tuple(matf['laser_properties']['laser_wavelength'])
    #     inst = cls(
    #         laser_properties=LaserProperties.from_dict(matf['laser_properties']),
    #         ad2_properties=AD2CaptDeviceProperties.from_dict(matf['ad2_properties']),
    #         wafer_properties=WaferProperties.from_dict(matf['wafer_properties']),
    #         waveguide_properties=WaveguidePropertiesMZI.from_dict(matf['waveguide_properties']),
    #         measurement_properties=MeasurementProperties.from_dict(matf['measurement_properties']),
    #         timestamp=matf['timestamp'],
    #         measurement_data=pd.DataFrame({
    #                         'wavelength': matf['wavelength'],
    #                         'amplitude': matf['amplitude'],
    #                         'amplitude_detrended': matf['amplitude_detrended']}),
    #
    #         #measurement_file=Path(f"{mat_file.absolute().parent}/{matf['measurement_file']}").absolute()
    #     )
    #     return inst
    #
    @staticmethod
    def convert(mat_file):
        """Reads the mat file and converts the new format to the old format"""
        data = SingleMeasuredData.from_mat(mat_file)
        filename = mat_file.name.replace('.mat', '_v2.mat')
        path = str(mat_file.parent).replace('measurements', 'measurements_v2')
        # create a folder converted and save the file there
        file = Path(f"{path}/{filename}")
        data.save(str(file))


    def __init__(self,
                 laser_properties: GenericProperties,
                 ad2_properties: GenericProperties,
                 wafer_properties: GenericProperties,
                 waveguide_properties: GenericProperties,
                 measurement_properties: GenericProperties,
                 timestamp: datetime,
                 measurement_file: Path | str = None,
                 measurement_data = None,
                 *args, **kwargs
                 ):
        super().__init__(laser_properties, ad2_properties, wafer_properties, waveguide_properties, measurement_properties)

        if isinstance(measurement_data, list) or isinstance(measurement_data, np.ndarray):
            self.measurement_file = measurement_file
            # Store ot
            self._measured_data: pd.DataFrame = self._tables.update(
                    pd.DataFrame(measurement_data, columns=['amplitude']), '_measured_data')
            self._measurement_length = len(self._measured_data)
            self.logger.debug(f"Measurement signal length: {self._measurement_length}")
            # Generate the wacelength vector
            self._create_wavelength_vector()
            # Detrend the signal
            self._detrend_signal()
        else:
            #self._raw_measurement_data: dask.array = dd.read_parquet(self.measurement_file)
            self._measured_data = self._tables.update(measurement_data, '_measured_data')


        self.print_enabled = True
        self._calculated = False
        # ==============================================================================================================
        self._timestamp = timestamp
        self._measure_time = self._ad2_properties.measurement_time

        self.datafile = None
        # Measured Data (raw)

        # self._measurement_data_smoothed = self._smooth_signal(self._measurement_data_detrend)

        # ==============================================================================================================
        # Dataframe with measured values

        # self._create_wavelength_vector()
        # self._detrend_signal()

    @property
    def measured_data(self):
        return self._measured_data

    @measured_data.setter
    def measured_data(self, value):
        self._measured_data = value

    # ==================================================================================================================
    # Generate a wavelength vector from the given settings
    # ==================================================================================================================
    def _create_wavelength_vector(self):
        """ 
            Creates the wavelength vector for the measured data.
            The wavelength vector is created based on the given laser properties.
        """
        
        sample_rate = float(self._ad2_properties.sample_rate)
        acc = float(self._laser_properties.acceleration)
        dec = float(self._laser_properties.deceleration)
        vel = float(self._laser_properties.velocity)
        wl_range = self._laser_properties.wavelength_range

        self.logger.debug(f"Creating wavelenght vector.")
        self.logger.debug(f"Velocity: {vel}, Acc: {acc}, Dec: {dec}, Range: {wl_range}")
        
        # the duration of a sample in s
        duration_sample = 1 / sample_rate
        t_acc = vel / acc  # Acceleration time of the laser; s
        t_dec = vel / dec  # Deceleration time of the laser; s
        self.logger.debug(f"duration_sample: {duration_sample}, t_acc: {t_acc}, Dec: {t_dec}")

        self.p_acc_stop = int(t_acc * sample_rate)
        self.logger.debug(f"Point acc_stop [{t_acc}*{sample_rate}]: {self.p_acc_stop}")

        self.p_dec_start = int(self._measurement_length - t_acc * sample_rate)
        self.logger.debug(f"Point dec_start [{self._measurement_length}-{t_acc}*{sample_rate}]: {self.p_dec_start}")

        if self.p_acc_stop > self.p_dec_start:
            raise ValueError("The Acceleration point cant be before the decceleration point: {self.p_acc_stop} > {self.p_dec_start}")
        
        s_acc = []
        for j in range(0, self.p_acc_stop):
            s_acc.append(
                ((1 / 2) * t_acc * (duration_sample * j) ** 2)
            )
        wl_acc = np.add(s_acc, float(wl_range[0]))
        self.logger.debug(f"Length of acc vector: {len(wl_acc)}")    
        wl_dec = np.subtract(float(wl_range[len(wl_range) - 1]),
                             s_acc)[::-1]
        self.logger.debug(f"Length of dec vector: {len(wl_dec)}")                     
        # Acceleration Phase/Deceleration Phase - Start and stop point
        self.wl_acc_stop = wl_acc[-1]
        self.wl_dec_start = wl_dec[0]
        #self.logger.debug(f"lenght: {self.p_dec_start} - {self.p_acc_stop}")
        length = int((self.p_dec_start - self.p_acc_stop))
        rounding_diff = self._measurement_length - (length + len(wl_acc) + len(wl_dec))
        length += rounding_diff
        self.logger.debug(f"0 {length}")
        # self.logger.debug(f"+1 {length+2}")
        #self.logger.debug(f"+3{length+3}")
        #length = length + 1
        # self.logger.debug(f"+1 {length}")
        wl_move = linspace(self.wl_acc_stop, self.wl_dec_start, length)
       
        wl = np.concatenate((wl_acc, wl_move, wl_dec))
        self.logger.debug(f"[{self}] | Created wavelength vector: [0 - {self.p_acc_stop}] (Diff {len(wl_acc)}) -- "
                          f"<{len(wl_move)}> -- "
                          f"[{self.p_dec_start} - {len(wl)}] (Diff {len(wl_dec)})")

        self._measured_data['wavelength'] = wl

    def _smooth_signal(self, vec, window=150):

        return np.convolve(vec, np.ones(window), 'valid') / window

    def _detrend_signal(self):
        self._measured_data['detrend'] = signal.detrend(self._measured_data['amplitude'])

    # ==================================================================================================================
    # Calculations and table creations
    # ==================================================================================================================
    def find_peaks(self):
        self._detrend_signal()
        vec = self._measured_data['detrend']
        _peaks, _ = find_peaks(vec,
                               height=self.measurement_properties.find_peaks.height,
                               distance=self.measurement_properties.find_peaks.distance,
                               prominence=self.measurement_properties.find_peaks.prominence)
        peaks = np.zeros(len(vec))
        peaks[_peaks] = 1
        self._measured_data['peaks'] = peaks.astype(bool)
        self._peaks = self._tables.update(self._measured_data[self._measured_data['peaks'] == True], '_peaks')
        self.logger.debug(f"[{self}] | Found {len(self._peaks)} peaks. "
                          f"Parameters {self.measurement_properties.find_peaks}")

    def calulate_all(self, recalculate=False):
        if not self._calculated or recalculate:
            self.logger.info(f"[{self}] | Recalculating measurements {str(self)}")

            self.find_peaks()
            self.calculate_wg_params()
            self._calculated = True

    # ==================================================================================================================
    # Filtering (old)
    # ==================================================================================================================
    def apply_filter(self):
        if not self._ad2_properties_set:
            raise Exception("AD2 properties not set. Please set them first.")

        if not self._laser_properties_set:
            raise Exception("Laser properties not set. Please set them first.")

        (
            self._filtered_amplitude,
            first_start, self.start_idx,
            first_end, self.end_idx,
            self.signal_end_expected,
            self.marker_start,
            self.marker_stop
        ) = self.filter_signal(self.measured_data, column='measurements')

        self.time_start_point = self.start_idx / self.ad2_sample_rate
        self.time_end_point = self.end_idx / self.ad2_sample_rate
        self.time_end_point_expected = self.signal_end_expected / self.ad2_sample_rate

        self._filtered_amplitude = self.assign_wavelength(self._filtered_amplitude, self.wavelength_range[0],
                                                          self.wavelength_range[1])
        self.signal_length = len(self._filtered_amplitude)

        # Sanity check if the found length is approximatly the same as the expected length
        tolerance = 0.025  # 2,5 % tolerance = 0.25 sec
        if 1 - abs(self.signal_end_expected / self.end_idx) > tolerance:
            raise Exception(
                f"The found signal length ({self.signal_end_expected})"
                f"is not approximatly the same as the expected signal length ({self.end_idx})."
            )

        return (self._filtered_amplitude,
                self.start_idx, self.time_start_point,
                self.end_idx, self.time_end_point,
                self.signal_end_expected, self.time_end_point_expected
                )

    def find_index(self, samples_sweep=None, keyword='filtered', threshold=0.0005, reverse_signal=False):
        rolling_keyword = 'rolling'
        marker = {
            'first_hit': 0,
            'steady_mean': 0,
            'steady_mean_pt': 0,
            'steady_mean_mt': 0,
            'steady_min': 0,
            'steady_max': 0,
            'window_for_mean': [0, 0],
            'window_for_search': [0, 0],
            'second_hit': 0,
        }
        if reverse_signal:
            self.logger.debug("[FILTER:FIND INDEX] Reversing the signal")
            samples = samples_sweep[::-1]
            samples = samples.reset_index(drop=True)
        else:
            samples = samples_sweep

        # create a new dataframe
        # Drop values that have been already marked as invalid
        samples = samples.dropna()

        # *****************************************************************************************
        # (1): Extract 200 ms and calculate a mean value. This will be used to find the
        # approximative start point of the signal.
        #      (1.1) Cut a part that we are sure is steady (e.g. 100 ms after the start up to 300ms)
        start_idx = int(self.ad2_sample_rate / 10)
        stop_idx = int((self.ad2_sample_rate / 10) * 3)
        sample_window_steady = samples[keyword][start_idx:stop_idx]
        self.logger.debug(
            "[FILTER:FIND INDEX:1.1] Extract 200 ms and find min and max values. start_idx %s, stop_idx %s" % (
                start_idx, stop_idx))
        #      (1.2) We now want to approximatly find the part where the signal starts rising or fluctuatig.
        #            This is, where the Signal is greater than our min or max values
        #            Also, store these values as a marker
        signal_min = float(sample_window_steady.min());
        marker['steady_min'] = signal_min
        signal_max = float(sample_window_steady.max());
        marker['steady_max'] = signal_max
        self.logger.debug(
            "[FILTER:FIND INDEX:1.2] Signal processed. signal_min %s, signal_max %s" % (signal_min, signal_max))
        #      (1.3) Extract the first approximate starting position. This is, where the signal exceed
        #             our min or max values. We have found the first approximate starting point.
        index_first_hit = samples[
            (samples[rolling_keyword] >= signal_max) | (samples[rolling_keyword] <= signal_min)
            ].first_valid_index()
        index_first_hit_abs = samples.index1[index_first_hit]
        self.logger.info(
            f"[FILTER:FIND INDEX:1.3] First index found at {index_first_hit_abs / self.ad2_sample_rate} sec. index_first_hit {int(index_first_hit_abs)}/{len(samples)} (rel: {index_first_hit})")

        # *****************************************************************************************
        # (2) Now we want to calculate a mean that is near our starting point. For this, we go back
        #     200 ms and calculate the mean of 200 ms. This should yield to a mean value that corresponds
        #     to our signal shortly bevor it starts.
        value = int(self.ad2_sample_rate / 10)
        if reverse_signal:
            start_idx = int(index_first_hit - value * 4)
            start_idx_abs = int(index_first_hit_abs + value * 2)
            stop_idx = int(index_first_hit - value * 2)
            stop_idx_abs = int(index_first_hit_abs + value * 4)
        else:
            start_idx = int(index_first_hit - value * 4)
            start_idx_abs = int(index_first_hit_abs - value * 4)
            stop_idx = int(index_first_hit - value * 2)
            stop_idx_abs = int(index_first_hit_abs - value * 2)

        window_for_mean = samples[keyword].loc[start_idx:stop_idx];
        marker['window_for_mean'] = [start_idx_abs, stop_idx_abs]
        self.logger.debug(
            "[FILTER:FIND INDEX:2.1] Extract 200 ms and calculate a new mean value. start_idx %s (rel %s), stop_idx %s (rel: %s). len <%s>"
            % (start_idx_abs, start_idx,
               stop_idx_abs, stop_idx, len(window_for_mean)))
        #      (2.1) Calculate the mean value of the 200 ms window
        signal_mean = float(window_for_mean.mean());
        marker['steady_mean'] = signal_mean
        self.logger.debug("[FILTER:FIND INDEX:2.2] Signal processed. signal_mean %s" % (signal_mean))

        # *****************************************************************************************
        # (3) Since we have found a mean value that hopefully cooresponds to our mean value of the steady
        #     part near our first starting point, we can try to find a more accurate starting point.
        #     Again, this si done by defining a threshold that, if exceeded, mark our new, more accurate starting point.
        treshold_max = signal_mean * (1 + threshold);
        marker['steady_mean_pt'] = treshold_max
        treshold_min = signal_mean * (1 - threshold);
        marker['steady_mean_mt'] = treshold_min
        self.logger.debug(
            "[FILTER:FIND INDEX:3.1] Defining new thresholds for mean: <%s>: treshold_max <%s>, treshold_min <%s>" % (
                signal_mean, treshold_max, treshold_min))

        #      (3.1) New get a window of our expected signal start. 
        #            self.print_m("[3]: dataframe 'samples_cut \n%s" % samples)
        value = int(self.ad2_sample_rate / 10)
        start_idx = int(index_first_hit - value)
        start_idx_abs = int(index_first_hit_abs - value)
        stop_idx = int(index_first_hit + value)
        stop_idx_abs = int(index_first_hit_abs + value)
        window_for_search = samples.loc[start_idx:stop_idx];
        marker['window_for_search'] = [start_idx_abs, stop_idx_abs]
        self.logger.debug(
            "[FILTER:FIND INDEX:3.2] Extract 200 ms around the starting point. start_idx %s (rel %s), stop_idx %s (rel: %s). len <%s>"
            % (start_idx_abs, start_idx, stop_idx_abs, stop_idx, len(window_for_search)))
        #     (3.2) Now we want to find the first point where the signal exceeds our threshold.
        index_second_hit = window_for_search[
            (window_for_search[rolling_keyword] > treshold_max) | (window_for_search[rolling_keyword] < treshold_min)
            ].first_valid_index()
        if index_second_hit is None:
            raise Exception("End of Signal not found. index_second_hit %s" % index_second_hit)
        #    (3.3) This window may have not the corrct indices. We need to get the correct one
        index_second_hit_abs = samples.index1[index_second_hit]
        self.logger.info(
            f"[FILTER:FIND INDEX:3.3] Second index found at {index_second_hit_abs / self.ad2_sample_rate} sec. index_second_hit {index_second_hit_abs}/{len(samples)} (rel: {index_second_hit})"
        )

        if index_second_hit == None:
            index_second_hit = 0
        else:
            index_second_hit = samples.index1[index_second_hit]
            marker['second_hit'] = index_second_hit
        index_first_hit = samples.index1[index_first_hit]
        marker['first_hit'] = index_first_hit

        return index_first_hit_abs, index_second_hit_abs, marker

    def filter_signal(self, measured_amplitude, column='measurements'):
        self.logger.info("[FILTER] Applying filter to given signal.")
        # Filter the first second of the measurement
        measured_amplitude = measured_amplitude.reset_index().rename({'index': 'index1'}, axis='columns')
        measured_amplitude['filtered'] = measured_amplitude[column]
        measured_amplitude.loc[:self.ad2_sample_rate] = None
        # Calculate the moving average
        measured_amplitude["rolling"] = measured_amplitude['filtered'].rolling(window=1000).mean().shift(
            -500)  # [1000-1:] # 0,01nm
        self.logger.debug(f"[FILTER] Total Length of given signal {len(measured_amplitude)}")

        first_start, second_start, marker_start = self.find_index(measured_amplitude, column)
        self.logger.info(f"[FILTER] Starting index found at {second_start} (first hit at {first_start}) ")
        measured_amplitude['filtered'].loc[:second_start] = None

        # Now we need to find the end of the signal. For this we assume, that the laser movement is "nearly" correct.
        # The laser waits approximatly 500 ms to move the laser back to it's starting position.
        index_signal_end_expected = int(second_start + (self.laser_movement_time * self.ad2_sample_rate))
        self.logger.debug(f"[FILTER] Expected end: {index_signal_end_expected}")

        # We found the expected length, the laser waits for 500 ms until moving back
        # We want to use this, to get the mean value of the amplitude of this specific wave length
        # For this we cut the signal 400 ms (= ad2_sample_rate * 0.4) after the expected end
        measured_amplitude['filtered'].loc[int(index_signal_end_expected + (self.ad2_sample_rate * 0.4)):] = None
        # Reverse the signal and do the same procedure again

        first_end, second_end, marker_stop = self.find_index(measured_amplitude, column, reverse_signal=True)
        self.logger.info(f"[FILTER] End index found at {second_end} (first hit at {first_end}).")
        measured_amplitude['filtered'].loc[second_end:] = None

        measured_amplitude.dropna(inplace=True)
        # measured_amplitude = measured_amplitude.drop(['index1'], axis = 1)
        filtered_aplitude = measured_amplitude.filter(['filtered'], axis=1).reset_index(drop=True)
        self.logger.info(
            f"[FILTER] AD2 sample rate: {self.ad2_sample_rate} samples/sec. "
            f"AD2 samples: {self.ad2_total_samples} samples. "
            f"AD2 measurement duration: {self.ad2_total_measurement_time} sec."
        )
        self.logger.info(
            f"[FILTER] Laser movement ({self.wavelength_range[0]}-{self.wavelength_range[1]}): {self.laser_movement_time} sec. "
            f"Laser velovity: {self.laser_velocity} m/s. "
            f"Laser samples expected: {self.laser_samples_expected} samples ({self.laser_samples_expected / self.ad2_sample_rate}) sec."
        )
        self.logger.info(
            f"[FILTER] Signal length {len(self._measured_data)} ({len(self._measured_data) / self.ad2_sample_rate} sec). "
            f"Start {second_start} ({second_start / self.ad2_sample_rate} sec). "
            f"End {second_end} ({second_end / self.ad2_sample_rate} sec). "
            f"Expected: {index_signal_end_expected} ({index_signal_end_expected / self.ad2_sample_rate} sec). "
            f"Diff {second_end - second_start} ({second_end / self.ad2_sample_rate - second_start / self.ad2_sample_rate} sec)."
        )

        # self.print_m(samples_sweep_down)
        return (filtered_aplitude,
                first_start, second_start,
                first_end, second_end,
                index_signal_end_expected,
                marker_start,
                marker_stop
                )

    def assign_wavelength(self, filtered_amplitude: list = None, wavelength_start: float = 850,
                          wavelength_stop: float = 855, start_point: int = None):
        measurment_points = len(filtered_amplitude)
        filtered_amplitude['wavelength'] = pd.Series(
            np.linspace(wavelength_start, wavelength_stop, measurment_points)
        )
        # filtered_amplitude.set_index('wavelength',inplace=True)
        # if start_point is None:
        #     # Get the number of measruement points (should be 50000):

        #     #self.print_m(measurment_points)

        #     #self.print_m(measured_amplitude)
        # else:
        #     # We need to assign the first n (up to the start_point) points the l
        #     end_point = start_point + self.laser_samples_expected
        #     filtered_amplitude['wavelength'] = 0
        #     filtered_amplitude.loc[0:start_point-1, 'wavelength'] = wavelength_start
        #     filtered_amplitude.loc[start_point:end_point, 'wavelength'] = pd.Series(
        #         np.linspace(wavelength_start, wavelength_stop, measurment_points)
        #     )
        #     filtered_amplitude.loc[end_point+1:measurment_points-1, 'wavelength'] = wavelength_stop

        return filtered_amplitude

    # ==================================================================================================================
    # To dicts
    # ==================================================================================================================
    def save(self, filename: str = None):
        self.filename = filename
        self._save_mat_file(self.filename)
        #self._save_measurement_parquet(self.measurement_file)

    def _save_measurement_parquet(self, filename: str = None):
        # Save the measurement file

        if filename is None:
            filename = self.filename
        filename = filename.replace('.mat', '.parquet')
        self.measurement_file = filename
        self._measured_data.to_parquet(self.measurement_file)
        self.logger.info(f"Saved measurement file to {self.measurement_file}")

    def to_dict(self) -> dict:
        return {
            "laser_properties": self._laser_properties.to_dict(),
            "ad2_properties": self._ad2_properties.to_dict(),
            "wafer_properties": self._wafer_properties.to_dict(),
            "measurement_properties": self._measurement_properties.to_dict(),
            #"waveguide_properties": self._waveguide_properties.to_dict(),
            #"measurement_file": str(Path(self.measurement_file).absolute().relative_to(Path(self._mat_filename).parent)),
            "amplitude": self._measured_data['amplitude'].to_list(),
            "wavelength": self._measured_data['wavelength'].to_list(),
            "amplitude_detrended": self._measured_data['detrend'].to_list(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "2.0.0"
        }

    # def flatten(self, parent_key='', sep='.'):
    #     items = []
    #     for key, value in self.to_dict().items():
    #         new_key = f"{parent_key}{sep}{key}" if parent_key else key
    #         if isinstance(value, dict):
    #             items.extend(self.flatten(new_key, sep=sep).items())
    #         else:
    #             items.append((new_key, value))
    #     return dict(items)

    def plot(self):

        downsample = 100
        filtered_amplitude_down = self._measured_data.copy()
        filtered_amplitude_down = filtered_amplitude_down[filtered_amplitude_down.reset_index().index % downsample == 0]
        # measured_amplitude = self.measured_amplitude.copy()
        # measured_amplitude = measured_amplitude[
        #    measured_amplitude.reset_index().index % downsample == 0]  # [240000:300000]
        # app.run_server(debug=True, port=8050)
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("filtered", "measurement")
        )
        fig.append_trace(
            go.Scatter(
                x=self._measured_data['wavelength'],
                y=self._measured_data['amplitude']),
            row=1, col=1
        )

        # fig.append_trace(
        #    go.Scatter(x=measured_amplitude.index, y=measured_amplitude['measurements']),
        #    row=2, col=1
        # )

        fig.add_vrect(x0=self.wl_acc_stop, x1=self.wl_dec_start, row=1, col=1,
                      annotation_text="valid: %s" % self._measurement_length, annotation_position="top left",
                      fillcolor="green", opacity=0.25, line_width=0)

        # fig.update_layout(title_text=str(self._wafer_nr))

        html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        # html += '</body></html>'

        with open('p_graph.html', 'a') as f:
            f.write(html)

        return html
        # fig.show()

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def enable_print(self, enable: bool = True):
        self.print_enabled = enable

    def print_m(self, *args, **kwargs):
        if self.print_enabled:
            self.logger.info(*args, **kwargs)


if __name__ == "__main__":
    app = QApplication()

    # Load a mat file from E:\03_Simulations\03_Simulations\measurements\Ary1 using scipy
    #setup_logging()
    # filename = r"E:\03_Simulations\03_Simulations\measurements\Ary1\Ary1_2021-03-10_15-00-00.mat"
    data1 = SingleMeasuredData.from_mat(
        r"support/measurement_die_22_struct_mzi2_2_20220306_1908_rep_11.mat"
    )
    data1.calulate_all()
    data1._save_mat_file(r'test.mat')

    data2 = SingleMeasuredData.from_mat_v2(r'test.mat')
    print("done")
