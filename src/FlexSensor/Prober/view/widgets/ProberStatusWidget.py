from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QStyle, QFrame, QProgressBar, QGroupBox

from FlexSensor import Prober


#from Prober.model.ProberModel import ProberModel


class ProberStatusWidget(QWidget):

    def __init__(self, model: Prober.Model):
        super().__init__()
        self.setFixedSize(300, 200)
        self.model = model
        self._grid_layout = QGridLayout()
        self.prober_status = self._add_status(self._get_std_icon("SP_ComputerIcon"), "", 0)
        self.version_status = self._add_status(self._get_std_icon("SP_MessageBoxInformation"), str(self.model.version), 1)
        self._add_line(2)
        self.errors = self._add_status(self._get_std_icon("SP_MessageBoxCritical"), "0", 3)
        self.warnings = self._add_status(self._get_std_icon("SP_MessageBoxWarning"), "0", 4)

        self._on_connected_changed(self.model.connected)

        self.model.signals.connected_changed.connect(self._on_connected_changed)
        self.model.signals.version_changed.connect(self._on_version_changed)
        self.model.signals.errors_changed.connect(self._on_errors_changed)
        self.model.signals.warnings_changed.connect(self._on_warnings_changed)


        self.setLayout(self._grid_layout)


    def _get_std_icon(self, icon_name) -> QIcon:
        return self.style().standardIcon(getattr(QStyle, icon_name))

    def _add_status(self, icon, text, pos=0):
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(50, 50))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(0, 0, 0, 0)
        # icon_label.setStyleSheet("background-color: rgb(192, 192, 192);")
        icon_label.setFixedSize(24, 24)
        icon_label.setScaledContents(True)

        text_label = QLabel(text)
        #text_label.setAlignment(Qt.AlignCenter)
        #text_label.setContentsMargins(0, 0, 0, 0)
        # text_label.setStyleSheet("background-color: rgb(192, 192, 192);")
        # text_label.setFixedSize(32, 50)
        #text_label.setScaledContents(True)

        self._grid_layout.addWidget(icon_label, pos, 0)
        self._grid_layout.addWidget(text_label, pos, 1)
        return text_label

    def _add_line(self, pos=0):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self._grid_layout.addWidget(line, pos, 0, 1, 2)

    def _on_connected_changed(self, connected):
        if connected:
            self.prober_status.setText("Connected")
        else:
            self.prober_status.setText("Disconnected")

    def _on_version_changed(self, version):
        self.version_status.setText(version)

    def _on_errors_changed(self, errors):
        self.errors.setText(str(len(errors)))

    def _on_warnings_changed(self, warnings):
        self.warnings.setText(str(len(warnings)))