import logging
import os
import pathlib
from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from FlexSensor.FlexSensorConfig import FlexSensorConfig
from FlexSensor.Prober.model import ProberModel


class MapFileParser:

    def __init__(self, model: ProberModel):
        self._map_path = self.open_map_file_dialog(Path(model.wafer_map))
        model.wafer_map = self._map_path
        with open(self._map_path, 'r') as file:
            self.result = self.parse_content(file.read())

    def open_map_file_dialog(self, file_path):
        file_path = pathlib.PurePosixPath(pathlib.Path(file_path).absolute())
        if not os.path.isfile(file_path):
            logging.info(f"Configuration file {file_path} not found")
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_path, _ = file_dialog.getOpenFileName(None, "Select a Configuration File", filter="*.map")
        if file_path != "":
            pass
            #vaut_config = FlexSensorConfig.load(file_path)
            #logging.info(f"Loading configuration file {file_path}")
        #logging.info(vaut_config)
        return file_path
    def parse_content(self, content):
        result = {}
        current_section = None

        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
            elif "=" in line and current_section is not None:
                key, value = line.split("=", 1)
                result.setdefault(current_section, {})
                result[current_section][key] = value

        return result


if __name__ == "__main__":
    parsed_map = MapFileParser("../Wafermapary1_48dies.map")
    print(parsed_map.result["Header"]["Description"])  # Output: Wafer Map File
    print(parsed_map.result["Wafer"]["Diameter"])  # Output: 200
    print(parsed_map.result["Bin"]["0"])  # Output: 1,a0,00C000,1,0,0,0,0