import logging
import os
import pathlib

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QFileDialog
from rich.logging import RichHandler

from FlexSensor.FlexSensorConfig import FlexSensorConfig
from FlexSensor.generics.ConsoleWindow import ConsoleWindow
from FlexSensor.pathes import image_root

import confighandler as Conf
class ApplicationInit:

    @staticmethod
    def set_icon(app):
        app_icon = QtGui.QIcon()
        app_icon.addFile(f'{image_root}/FlexSensorIcon.png', QtCore.QSize(16, 16))
        app_icon.addFile(f'{image_root}/FlexSensorIcon.png', QtCore.QSize(24, 24))
        app_icon.addFile(f'{image_root}/FlexSensorIcon.png', QtCore.QSize(32, 32))
        app_icon.addFile(f'{image_root}/FlexSensorIcon.png', QtCore.QSize(48, 48))
        app_icon.addFile(f'{image_root}/FlexSensorIcon.png', QtCore.QSize(256, 256))
        app.setWindowIcon(app_icon)

    @staticmethod
    def load_config_file(file_path):
        file_path = pathlib.PurePosixPath(pathlib.Path(file_path).absolute())
        if not os.path.isfile(file_path):
            logging.info(f"Configuration file {file_path} not found")
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_path, _ = file_dialog.getOpenFileName(None, "Select a Configuration File")
        # check if file dialog cancle was clicked
        vaut_config = FlexSensorConfig()
        if file_path != "":
            vaut_config = FlexSensorConfig.load(file_path)
            logging.info(f"Loading configuration file {file_path}")
        logging.info(vaut_config)
        return vaut_config

    @staticmethod
    def setup_logging(window: ConsoleWindow = None):
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != '<module name>':
                log_obj.disabled = True
        # Format the Rich logger
        FORMAT = "%(message)s"
        if window is not None:
            logging.basicConfig(
                level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                    RichHandler(rich_tracebacks=True), window.handler
                ]
            )
        else:
            logging.basicConfig(
                level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                    RichHandler(rich_tracebacks=True)
                ]
            )