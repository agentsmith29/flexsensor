import numpy as np
from numpy import ndarray

from generics.GenericProperties import GenericProperties


class WaferProperties(GenericProperties):
    def __init__(self,
                 wafer_number: str, structure_name: str,
                 die_nr: int, chuck_col: int, chuck_row: int,
                 structure_in: tuple, structure_out: tuple,
                 repetitions: int
                 ):
        super().__init__()
        self._structure_name = self.to_str(structure_name)
        self._wafer_number = self.to_str(wafer_number)

        self._die_number = self.to_int(die_nr[0])
        self._chuck_col = self.to_int(chuck_col[0])
        self._chuck_row = self.to_int(chuck_row[0])

        self._structure_in = self.to_tuple(structure_in)
        self._structure_out = self.to_tuple(structure_out)
        self._structure_x_in = int(self._structure_in[0])
        self._structure_y_in = int(self._structure_in[1])
        self._structure_x_out = int(self._structure_out[0])
        self._structure_y_out = int(self._structure_out[1])

        self._repetitions: int = self.to_int(repetitions)

    @property
    def repetition(self):
        return int(self._repetitions)

    @property
    def chuck_col(self):
        return int(self._chuck_col)

    @property
    def chuck_row(self):
        return int(self._chuck_row)

    @property
    def wafer_number(self) -> str:
        return str(self._wafer_number)

    @property
    def structure_x_in(self):
        return int(self._structure_x_in)

    @property
    def structure_y_in(self):
        return int(self._structure_y_in)

    @property
    def structure_x_out(self):
        return int(self._structure_x_out)

    @property
    def structure_name(self):
        return str(self._structure_name)

    @property
    def die_number(self) -> int:
        return int(self._die_number)

    @property
    def structure_y_out(self):
        return int(self._structure_y_out)

    @property
    def structure_in(self):
        return tuple(self._structure_in)

    @property
    def structure_out(self):
        return tuple(self._structure_out)

    @property
    def chuck_row(self):
        return int(self._chuck_row)

    def fields(self) -> dict:
        return {
            'wafer_number': self.wafer_number,
            'die_number': self.die_number,
            'structure_name': self.structure_name,
            'repetition': self.repetition,
            'structure_in': self.structure_in,
            'structure_out': self.structure_out,
            'chuck_col': self.chuck_col,
            'chuck_row': self.chuck_row

        }