from PySide6.QtCore import QObject
from numpy import ndarray


class GenericProperties(QObject):
    def __init__(self):
        super().__init__()

    def to_str(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return str(value[0])
        else:
            return str(value)

    def to_int(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return int(value[0])
        else:
            return int(value)

    def to_float(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return float(value[0])
        else:
            return float(value)

    def to_tuple(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return tuple(value[0])
        else:
            return tuple(value)

    def fields(self) -> dict:
      raise NotImplementedError
