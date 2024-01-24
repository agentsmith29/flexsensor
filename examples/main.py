# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
import logging
import sys
import time

from PySide6.QtWidgets import QApplication
# set env variable VELOX_SIM=TRUE
# to use the simulator instead of the real hardware
import os

os.environ["VELOX_SIM"] = "TRUE"

sys.path.append('./src')
from MeasurementRoutine import MeasurementRoutine
import FlexSensor


def main(argv):
    FlexSensor.ApplicationInit.setup_logging()
    logging.info(f"Starting Velox GUI Version {FlexSensor.__version__}")
    app = QApplication(sys.argv)
    splash_screen = FlexSensor.SplashScreen._display_splash_screen()
    splash_screen.show()
    app.processEvents()

    # Disable loggers that are not needed (e. g. numpy, etc)
    cw = FlexSensor.ConsoleWindow(app)
    # cw.show()

    # FlexSensor.ApplicationInit.setup_logging(cw)
    FlexSensor.ApplicationInit.set_icon(app)

    # Read the inital config file
    config = FlexSensor.ApplicationInit.load_config_file(f"{FlexSensor.configs_root}/init_config.yaml")
    config.autosave(enable=True, path="autosave_configs/init_config.yaml")

    # Start the main application
    main_model = FlexSensor.MainThreadModel(config=config)
    main_controller = FlexSensor.MainThreadController(main_model)
    # Register your measurement routine here
    main_controller.load_measurement_routine(MeasurementRoutine,
                                             ad2device=main_model.ad2_controller,
                                             laser=main_model.laser_controller,
                                             )
    main_window = FlexSensor.MainWindow(main_model, main_controller)




    main_window.show()
    splash_screen.finish(main_window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main(sys.argv)
