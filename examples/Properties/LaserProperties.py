import sys

#import mcpy

#sys.path.append('../mcpy/mcpy')
import mcpy

from FlexSensor.generics.GenericProperties import GenericProperties


class LaserProperties(GenericProperties):

    def __init__(self, acceleration: mcpy.Uncertainty, deceleration: mcpy.Uncertainty, velocity: mcpy.Uncertainty,
                 wavelength_range: tuple):
        super().__init__()
        # Laser properties
        self._acceleration: mcpy.Uncertainty = acceleration
        self._deceleration: mcpy.Uncertainty = deceleration
        self._velocity: mcpy.Uncertainty = velocity
        self._wavelength_range: list | tuple = wavelength_range

    @property
    def deceleration(self) -> mcpy.Uncertainty:
        return self._deceleration

    @deceleration.setter
    def deceleration(self, value):
        self._deceleration = value

    @property
    def velocity(self) -> mcpy.Uncertainty:
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def wavelength_range(self) -> mcpy.Uncertainty:
        return self._wavelength_range

    @wavelength_range.setter
    def wavelength_range(self, value):
        self._wavelength_range = value

    @property
    def acceleration(self) -> mcpy.Uncertainty:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    def to_dict(self) -> dict:
        return {
            'deceleration': 1.997,#float(self.deceleration),
            'velocity': 1.002,#float(self.velocity),
            'wavelength_range': [840, 860],  # .to_tuple(),
            'acceleration': 1.997 #float(self.acceleration)
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            acceleration=mcpy.Uncertainty.from_dict(d['acceleration']),
            deceleration=mcpy.Uncertainty.from_dict(d['deceleration']),
            velocity=mcpy.Uncertainty.from_dict(d['deceleration']),
            wavelength_range=()
        )
