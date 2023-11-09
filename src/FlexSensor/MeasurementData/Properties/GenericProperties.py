import pandas as pd
from PySide6.QtCore import QObject
from numpy import ndarray

class GenericProperties(QObject,):

    def __init__(self):

        super().__init__()

    def to_str(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return self.to_str(value[0])
        else:
            return str(value)

    def to_int(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return self.to_int(value[0])
        else:
            return int(value)

    def to_float(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return self.to_float(value[0])
        else:
            return float(value)

    def to_tuple(self, value):
        if (isinstance(value, list) or isinstance(value, ndarray)) and len(value) == 1:
            return tuple(value[0])
        else:
            return tuple(value)

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(self, data: dict):
        raise NotImplementedError

    def to_sql(self, engine):
        self.metadata.create_all(engine)
        "Create a  relational table in the database with the given engine"
        with Session(engine) as session:
            session.add(self)
            session.commit()
        # df = pd.DataFrame(self.to_dict())
        # df.to_sql(table_name, engine, if_exists='append', index=False)
