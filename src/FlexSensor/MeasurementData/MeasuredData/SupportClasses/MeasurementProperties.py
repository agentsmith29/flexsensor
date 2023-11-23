import numpy as np
from PySide6.QtCore import Signal

#import mcpy
#from mcpy import Uncertainty

from generics.GenericProperties import GenericProperties


class MPropertiesFindPeaks(GenericProperties):
    properties_changed = Signal()

    def __init__(self, prominence: float | None, distance: float | None, height: float | None):
        super().__init__()
        self.set_properties(prominence, distance, height)

    def set_properties(self, prominence: float | None, distance: float | None, height: float | None):
        self._prominence = prominence
        self._distance = distance
        self._height = height
        self.properties_changed.emit()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.properties_changed.emit()

    @property
    def prominence(self):
        return self._prominence

    @prominence.setter
    def prominence(self, value):
        self._prominence = value
        self.properties_changed.emit()

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
        self.properties_changed.emit()

    def fields(self) -> dict:
        return {
            'prominence':  self.prominence if self.prominence is not None else np.NaN,
            'distance': self.distance if self.prominence is not None else np.NaN,
            'height': self.height if self.height is not None else np.NaN,
        }

    def __str__(self):
        return f"h: {self.height} - d: {self.distance} - p: {self.prominence}"


class WaveguideProperties(GenericProperties):
    def __init__(self, length: Uncertainty, width: Uncertainty, height: Uncertainty):
        super().__init__()
        self._length: Uncertainty = length
        self._width: Uncertainty = width
        self._height: Uncertainty = height

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    def fields(self) -> dict:
        return {
            'width':  self.width.to_tuple(),
            'length': self.length.to_tuple(),
            'height': self.height.to_tuple(),
        }

class WaveguidePropertiesMZI(WaveguideProperties):
    def __init__(self, length1: Uncertainty, length2: Uncertainty, width: Uncertainty, height: Uncertainty):

        self._arm1 = WaveguideProperties(length1, width, height)
        self._arm2 = WaveguideProperties(length2, width, height)
        super().__init__(mcpy.Uncertainty(float(self._arm1.length) - float(self._arm2.length)), width, height)

    @property
    def length_diff(self):
        return self._length_diff

    @length_diff.setter
    def length_diff(self, value):
        self._length_diff = value

    @property
    def arm1(self):
        return self._arm1

    @arm1.setter
    def arm1(self, value):
        self._arm1 = value

    @property
    def arm2(self):
        return self._arm2

    @arm2.setter
    def arm2(self, value):
        self._arm2 = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    def fields(self) -> dict:
        return {
            'width':  self.width,
            'length': self.length,
            'arm1': self.arm1,
            'arm2': self.arm2
        }

class WaveguidePropertiesMRR(WaveguideProperties):
    def __init__(self, length, width: float, radius, gap: float):
        super().__init__()
        super().__init__(length, width)
        self._radius = radius
        self._gap = gap

    @property
    def length_diff(self):
        return self._length_diff

    @length_diff.setter
    def length_diff(self, value):
        self._length_diff = value

    @property
    def arm1(self):
        return self._arm1

    @arm1.setter
    def arm1(self, value):
        self._arm1 = value

    @property
    def arm2(self):
        return self._arm2

    @arm2.setter
    def arm2(self, value):
        self._arm2 = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value


class MeasurementProperties(GenericProperties):
    def __init__(self, find_peaks_properties: MPropertiesFindPeaks):
        super().__init__()
        self._find_peaks = find_peaks_properties

    @property
    def find_peaks(self):
        return self._find_peaks

    @find_peaks.setter
    def find_peaks(self, value):
        self._find_peaks = value

    def fields(self) -> dict:
        return {
            'find_peaks': self.find_peaks.fields(),
            'test': 1
        }
