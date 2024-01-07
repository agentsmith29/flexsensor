import logging
import sys

from PySide6.QtGui import QWindow
from PySide6.QtWidgets import QGridLayout, QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout

import confighandler as Config

#from MapFileParser import MapFileParser
from FlexSensor.Prober.controller.ProberController import ProberController
from FlexSensor.Prober.model.ProberModel import ProberModel
from FlexSensor.Prober.view.widgets.DieGridWidget import DieGridWidget
from FlexSensor.Prober.view.widgets.ProberPositionWidget import ProberPositionWidget
from FlexSensor.Prober.view.widgets.ProberStatusWidget import ProberStatusWidget


class ProberControlWindow(QMainWindow):

    def __init__(self, model: ProberModel, controller: ProberController):
        super().__init__()
        self.controller = controller
        self.model = model

        #self.parsed_map = MapFileParser(self.controller.wafer_map)

        # Add a GridLayout to the main window
        self._widget = QWidget()
        self._grid_layout = QGridLayout()
        # Add the DieGridWidget to the main window
        # Add the prober status widget to the a group box
        groupbox_status_widget = QGroupBox("Prober Status")
        groupbox_status_widget_layout = QVBoxLayout()
        groupbox_status_widget_layout.addWidget(ProberStatusWidget(self.model))
        groupbox_status_widget.setLayout(groupbox_status_widget_layout)


        groupbox_position_widget = QGroupBox("Prober Status")
        groupbox_position_widget_layout = QVBoxLayout()
        groupbox_position_widget_layout.addWidget(ProberPositionWidget(self.model))
        groupbox_position_widget.setLayout(groupbox_position_widget_layout)

        self._grid_layout.addWidget(groupbox_status_widget, 0, 0, 1, 1)
        self._grid_layout.addWidget(groupbox_position_widget, 1, 0, 1, 1)
        self._grid_layout.addWidget(DieGridWidget(self.model), 0, 1, 2, 1)
        # set the layout of the main window
        self._widget.setLayout(self._grid_layout)
        self.setCentralWidget(self._widget)




if __name__ == "__main__":
    #setup_logging()
    logging.warning("ProberControlWindow.py is not meant to be run as a script.")

    app = QApplication()

    vaut_config = VAutomatorConfig.load_config("../configs/init_config.yaml")

    prober_model = ProberModel()
    prober_controller = ProberController(prober_model, vaut_config)
    main_window = ProberControlWindow(prober_controller, prober_model)
    # test_win = StructureSelector()

    main_window.show()
    sys.exit(app.exec())
