import logging
import time
from dataclasses import dataclass
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import Dict, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QWidget

import MeasurementEvaluationTool as met
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData

from wrappers.QProgressBarWindow import QProgressBarWindow


class MeasurementDataLoader(QWidget):

    @staticmethod
    def glob_files(path, glob):
        """Recursively glob for files in a directory and subdirectories. Returns a list of paths"""
        # use list comprehension and rglob
        return [f for f in Path(path).rglob(glob)]

    @classmethod
    def from_folder(cls, path, to_database):
        logging.info(f"Opening path {path}")
        files = MeasurementDataLoader.glob_files(path, "*.mat") #[Path(f"{path}/{f}").absolute() for f in listdir(path) if isfile(join(path, f)) and ".mat" in f]
        logging.info(f"Found {len(files)}.")

        mea_list = []
        for i, f, it in QProgressBarWindow(files):
            it.print(f"Loading measurement {str(f.name)}")

            #try:
                #mea_list.append(SingleMeasuredData.from_mat_v2(f))
            to_database.add_data(SingleMeasuredData.from_mat_v2(f))
            #except Exception as e:
            #    logging.error(f"Could not load file {f.name}: {e}")

        return cls(mea_list)

    def __init__(self, data: list[SingleMeasuredData]):
        super().__init__()
        self._data = data
        self.logger = logging
        self._wafers = set()
        self._dies = set()
        self._structure_name = set()
        self._sorted_files = self.classify(self._data)
        # Now  classify

    @property
    def structure_name(self) -> set[str]:
        return self._structure_name

    @property
    def sorted_files(self) -> dict[str, dict[int, dict[Any, list[SingleMeasuredData]]]]:
        return self._sorted_files

    @property
    def dies(self) -> set[int]:
        return self._dies

    @property
    def wafers(self) -> set[str]:
        return self._wafers

    def classify(self, measurement_data: list[SingleMeasuredData]):
        sorted_files = {}
        for i, measurement, it in QProgressBarWindow(measurement_data):
            it.print(f"Classifying {measurement}")
            self.add_to_list(sorted_files, measurement)
        return sorted_files

    def get_measurement_series(self, wafer_number=None, die_number=None, structure_name=None) -> list[SingleMeasuredData]:
        if wafer_number is None and len(self._sorted_files.keys()) > 1:
            raise Exception(f"Wafer Number is ambiguous ({len(self._sorted_files)} possibilities). "
                            f"Please specify the wafer number!")
        elif wafer_number is None:
            wafer_number = list(self._sorted_files.keys())[0]
            print(f"Wafer Number is not ambiguous. Selected wafer number {wafer_number}")

        if die_number is None and len(self._sorted_files[wafer_number]) > 1:
            raise Exception(f"Die Number is ambiguous ({len(self._sorted_files[wafer_number])} possibilities). "
                            f"Please specify the wafer number!")
        elif die_number is None:
            die_number = list(self._sorted_files[wafer_number].keys())[0]
            print(f"Die Number is not ambiguous. Selected die number {die_number}")

        if structure_name is None and len(self._sorted_files[wafer_number][die_number]) > 1:
            raise Exception(f"Structure name is ambiguous ({len(self._sorted_files[wafer_number][die_number])} "
                            f"possibilities). Please specify the structure name!")
        elif structure_name is None:
            structure_name = list(self._sorted_files[wafer_number][die_number].keys())[0]
            print(f"Structure name is not ambiguous. Selected structure name {structure_name}")

        return self._sorted_files[wafer_number][die_number][structure_name]

    def get_measurement(self, repetition, wafer_number=None, die_number=None, structure_name=None, ) -> SingleMeasuredData:
        return self.get_measurement_series(wafer_number, die_number, structure_name)[repetition]

    def add_to_list(self, sorted_files: dict, measurement: SingleMeasuredData):
        """
            Adds a measurement to the measurement list
        """
        wafer_number = measurement.wafer_properties.wafer_number
        die_number = measurement.wafer_properties.die_number
        structure_name = measurement.wafer_properties.structure_name


        if (wafer_number in sorted_files and
                die_number in sorted_files[wafer_number] and
                structure_name in sorted_files[wafer_number][die_number]):
            sorted_files[wafer_number][die_number][structure_name].append(measurement)
        elif (wafer_number in sorted_files and
              die_number not in sorted_files[wafer_number]):
            sorted_files[wafer_number][die_number] = {structure_name: [measurement]}
        elif (wafer_number in sorted_files and
              die_number in sorted_files[wafer_number] and
              structure_name not in sorted_files[wafer_number][die_number]):
            sorted_files[wafer_number][die_number][structure_name] = [measurement]
        else:
            sorted_files[wafer_number] = {die_number: {structure_name: [measurement]}}
        self._wafers.add(wafer_number)
        self._dies.add(die_number)
        self._structure_name.add(structure_name)

if __name__ == "__main__":
    mypath = r'E:\test_measurements'
    mm_data = MeasurementDataLoader(mypath)
