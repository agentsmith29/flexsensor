# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version:
"""
import logging
from pathlib import Path

import confighandler as cfg

from .AppSettings import AppSettings
from FlexSensor.WaferConfig import WaferConfig

import LaserControl as Laser
import CaptDeviceControl as CaptDevice

class FlexSensorConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.wafer_version = cfg.Field("MaskARY1_Jakob_full", friendly_name="Wafer Version",
                                     description="Wafer Version to be measured")
        self.wafer_number = cfg.Field("T40741W177G0", friendly_name="Wafer Number",
                                      description="Wafer Number to be measured")

        self.output_directory = cfg.Field(Path("./"), friendly_name="Output Directory",
                                     description="Measurement output directory")

        self.log_file = cfg.Field("fs.log", friendly_name="Log File",
                                          description="")

        self.wafer_config = WaferConfig()
        self.app_config = AppSettings()
        self.laser_config = Laser.Config()
        self.captdev_config = CaptDevice.Config()

        self.register()

