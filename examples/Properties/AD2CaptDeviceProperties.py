import pandas as pd

from FlexSensor.generics.GenericProperties import GenericProperties


class AD2CaptDeviceProperties(GenericProperties):

    def __init__(self, samples_lost: float, samples_corrupted: float,
                 acquisition_rate: float, n_samples: int,
                 measurement_time: float):
        super().__init__()
        # Laser properties
        self._samples_lost: float = self.to_float(samples_lost)
        self._samples_currputed: float = self.to_float(samples_corrupted)
        self._sample_rate: float = self.to_float(acquisition_rate)
        self._n_samples: int = self.to_int(n_samples)
        self._measurement_time: float = self.to_float(measurement_time)

    @property
    def samples_lost(self):
            return self._samples_lost

    @samples_lost.setter
    def samples_lost(self, value):
            self._samples_lost = value

    @property
    def samples_corrupted(self):
            return self._samples_currputed

    @samples_corrupted.setter
    def samples_corrupted(self, value):
            self._samples_currputed = value

    @property
    def n_samples(self):
            return self._n_samples

    @n_samples.setter
    def n_samples(self, value):
            self._n_samples = value

    @property
    def measurement_time(self):
            return self._measurement_time

    @measurement_time.setter
    def measurement_time(self, value):
            self._measurement_time = value

    @property
    def sample_rate(self):
            return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
            self._sample_rate = value


    def to_dict(self) -> dict:
        return {
            'samples_lost': self.samples_lost,
            'samples_corrupted': self.samples_corrupted,
            'n_samples': self.n_samples,
            'measurement_time': self.measurement_time,
            'acquisition_rate': self.sample_rate
        }

    @classmethod
    def from_dict(cls, mat_struct):
        return cls(
            samples_lost=mat_struct['samples_lost'],
            samples_corrupted=mat_struct['samples_corrupted'],
            acquisition_rate=mat_struct['acquisition_rate'],
            n_samples=mat_struct['n_samples'],
            measurement_time=mat_struct['measurement_time']
        )


