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

sys.path.append('./src')
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
    #cw.show()

    #FlexSensor.ApplicationInit.setup_logging(cw)
    FlexSensor.ApplicationInit.set_icon(app)

    # Read the inital config file

    config = FlexSensor.ApplicationInit.load_config_file(f"{FlexSensor.configs_root}/init_config.yaml")
    config.autosave(enable=True, path="autosave_configs/init_config.yaml")


    main_model = FlexSensor.MainThreadModel(config=config)
    #wdg = config.view.widget()
    #wdg.show()
    main_controller = FlexSensor.MainThreadController(main_model)
    main_window = FlexSensor.MainWindow(main_model, main_controller)

    # test_win = StructureSelector()
    #config.save(f"{FlexSensor.configs_root}/init_config.yaml")
    main_window.show()
    splash_screen.finish(main_window)

    sys.exit(app.exec())

if __name__ == "__main__":

    main(sys.argv)


