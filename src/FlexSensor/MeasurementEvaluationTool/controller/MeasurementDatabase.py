import pickle
import sqlite3

from PySide6.QtWidgets import QApplication

from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
from generics.logger import setup_logging


class MeasurementDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS single_measured_data (
                wafer_number INTEGER,
                die_number INTEGER,
                structure_name TEXT,
                rep INTEGER,
                amplitude TEXT,
                wavelength TEXT
            )
        ''')
        self.conn.commit()

    def add_data(self, data: SingleMeasuredData):
        query = '''
            INSERT INTO single_measured_data (
                wafer_number,
                die_number,
                structure_name,
                rep,
                data_instance
            ) VALUES (?, ?, ?, ?, ?)
        '''
        values = (
            data.wafer_properties.wafer_number,
            data.wafer_properties.die_number,
            data.wafer_properties.structure_name,
            data.wafer_properties.repetition,
            pickle.dumps(data)
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_data(self, wafer_number, die_number):
        query = '''
            SELECT * FROM single_measured_data
            WHERE wafer_number = ? AND die_number = ?
        '''
        values = (wafer_number, die_number)
        self.cursor.execute(query, values)
        rows = self.cursor.fetchall()
        data_list = []
        for row in rows:
            amplitude = list(map(float, row[4].split()))
            wavelength = list(map(float, row[5].split()))
            data = SingleMeasuredData(row[0], row[1], row[2], row[3], amplitude, wavelength)
            data_list.append(data)
        return data_list

    def delete_data(self, wafer_number, die_number):
        query = '''
            DELETE FROM single_measured_data
            WHERE wafer_number = ? AND die_number = ?
        '''
        values = (wafer_number, die_number)
        self.cursor.execute(query, values)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    app = QApplication()
    setup_logging()

    db = MeasurementDatabase("data.db")
    # Load a measurement data
    file = (r'F:\measurements_v2_06032022\measurements_v2_06032022\mea_mrr1_1_2022_03_04\T40741W177G0\MaskARY1_Jakob\measurement\measurement_die_22_struct_mrr1_1_20220304_2249_rep_2_v2.mat')


    data = SingleMeasuredData.from_mat_v2(file)
    db.add_data(data)
    data_list = db.get_data(1, 2)
    print(data_list)
    db.delete_data(1, 2)
    data_list = db.get_data(1, 2)
    print(data_list)
    db.close_connection()