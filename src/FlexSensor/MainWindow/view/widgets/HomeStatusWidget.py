import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLineEdit, QLabel, QProgressBar

import __version__
from MainWindow.view import MainView
from Prober.view.widgets.ProberPositionWidget import ProberPositionWidget


class HomeStatusWidget(QWidget):

    def __init__(self, view: MainView):
        super().__init__()

        self.velox_kernel_version = None
        self.python_version = None
        self.script_version = None

        self.view: MainView = view
        layout = QGridLayout()
        layout.addWidget(self.init_UI_wafer_info(), 0, 0, 1, 1)
        layout.addWidget(self.init_UI_status_wdg(), 0, 1, 1, 1)
        layout.addWidget(self.init_UI_version_info(), 1, 0, 1, 2)

        self.setLayout(layout)

    def init_UI_wafer_info(self):

        grid_group_box = QGroupBox()
        layout = QGridLayout()

        self.tb_wafer_version = QLineEdit(parent=self, text=str(self.view.model.vaut_config.wafer_version))
        #self.tb_wafer_version.textChanged.connect(self.on_wafer_version_changed)
        layout.addWidget(QLabel("Wafer Version"), 0, 0, 1, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_wafer_version, 1, 0, 1, 2)  # row, column, rowspan, colspan

        self.tb_wafer_nr = QLineEdit(parent=self, text=str(self.view.model.vaut_config.wafer_nr))
        #self.tb_wafer_nr.textChanged.connect(self.on_wafer_nr_changed)
        layout.addWidget(QLabel("Wafer number"), 0, 2, 1, 1)
        layout.addWidget(self.tb_wafer_nr, 1, 2, 1, 2)

        grid_group_box.setLayout(layout)

        return grid_group_box

    def init_UI_status_wdg(self):
        grid_group_box = QGroupBox()
        layout = QVBoxLayout()
        layout.addWidget(ProberPositionWidget(self.view.model.prober_model, "Horizontal"))

        self.progress = QProgressBar(self)
        self.progress.setStyleSheet(
            "#GreenProgressBar { min-height: 12px; max-height: 12px; border-radius: 6px;}")
        layout.addWidget(self.progress)
        self.progress.setFixedHeight(self.progress.sizeHint().height() / 2)

        grid_group_box.setLayout(layout)

        return grid_group_box

    def init_UI_version_info(self):

        grid_group_box = QGroupBox()
        layout = QGridLayout()
        try:
            self.velox_kernel_version = QLineEdit(parent=self,
                                                  text=self.view.model.prober_model.report_velox_kernel_version())

        except Exception as e:
            print(e)
            self.velox_kernel_version = QLineEdit(
                parent=self, text="Velox kernel version not available")

        self.velox_kernel_version.setReadOnly(True)
        # self.velox_kernel_version.setEnabled(False)
        layout.addWidget(QLabel("Velox Kernel Version"), 2, 0)
        layout.addWidget(self.velox_kernel_version, 3, 0)

        self.python_version = QLineEdit(parent=self, text=str(sys.version))
        self.python_version.setReadOnly(True)
        # self.python_version.setEnabled(False)
        layout.addWidget(QLabel("Python Version"), 2, 1)
        layout.addWidget(self.python_version, 3, 1)

        self.script_version = QLineEdit(parent=self, text=__version__.__version__)
        self.script_version.setReadOnly(True)
        self.script_version.setEnabled(False)
        layout.addWidget(QLabel("Script Version"), 2, 2)
        layout.addWidget(self.script_version, 3, 2)

        grid_group_box.setLayout(layout)

        return grid_group_box
