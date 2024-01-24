from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, QProgressBar

from FlexSensor import Prober


#from Prober.model.ProberModel import ProberModel


class ProberPositionWidget(QWidget):

    def __init__(self, model: Prober.Model, chuck_position="Vertical"):
        super().__init__()
        self.model = model
        self.layout = QGridLayout()
        self.chuck_position = chuck_position

        self.lbl_chuck_x = QLabel()
        self.lbl_chuck_y = QLabel()
        self.lbl_chuck_z = QLabel()

        self.lbl_die_no = QLabel()
        self.lbl_structure = QLabel()
        self.lbl_die_col = QLabel()
        self.lbl_die_row = QLabel()

        self.lbl_die_no.setText(str(self.model.die))
        self.lbl_structure.setText("<b>Stopped</b>")
        self.lbl_die_col.setText(str(self.model.die_col))
        self.lbl_die_row.setText(str(self.model.die_row))
        self.lbl_chuck_x.setText(str(self.model.chuck_x))
        self.lbl_chuck_y.setText(str(self.model.chuck_y))
        self.lbl_chuck_z.setText(str(self.model.chuck_z))

        # self.progress = QProgressBar(self)
        # self.progress.setStyleSheet(
        #     "#GreenProgressBar { min-height: 12px; max-height: 12px; border-radius: 6px;}")
        # self.layout.addWidget(self.progress, 2, 0, 1, 4)
        # self.progress.setFixedHeight(self.progress.sizeHint().height() / 2)

        self._init_ui_wafer_position()
        self._init_ui_chuck_position()
        self.setLayout(self.layout)

        self.model.signals.chuck_x_changed.connect(self._on_chuck_x_changed)
        self.model.signals.chuck_y_changed.connect(self._on_chuck_y_changed)
        self.model.signals.chuck_z_changed.connect(self._on_chuck_z_changed)
        self.model.signals.die_changed.connect(self._on_die_no_changed)
        #self.model.signals.st.connect(self._on_structure_changed)
        self.model.signals.curr_die_col_changed.connect(self._on_die_col_changed)
        self.model.signals.curr_die_row_changed.connect(self._on_die_row_changed)


    def _init_ui_wafer_position(self):
        self.layout.addWidget(QLabel("Die No:"), 0, 0)
        self.layout.addWidget(self.lbl_die_no, 0, 1)

        self.layout.addWidget(QLabel("Structure"), 0, 2)
        self.layout.addWidget(self.lbl_structure, 0, 3)

        self.layout.addWidget(QLabel("Die col:"), 1, 0)
        self.layout.addWidget(self.lbl_die_col, 1, 1)

        self.layout.addWidget(QLabel("Die row:"), 1, 2)
        self.layout.addWidget(self.lbl_die_row, 1, 3)

    def _init_ui_chuck_position(self):
        if self.chuck_position == "Vertical":
            self.layout.addWidget(QLabel("X"), 2, 0)
            self.layout.addWidget(self.lbl_chuck_x, 2, 1)

            self.layout.addWidget(QLabel("Y"), 3, 0)
            self.layout.addWidget(self.lbl_chuck_y, 3, 1)

            self.layout.addWidget(QLabel("Z"), 4, 0)
            self.layout.addWidget(self.lbl_chuck_z, 4, 1)

        elif self.chuck_position == "Horizontal":
            self.layout.addWidget(QLabel("X"), 2, 0)
            self.layout.addWidget(self.lbl_chuck_x, 2, 1)

            self.layout.addWidget(QLabel("Y"), 2, 2)
            self.layout.addWidget(self.lbl_chuck_y, 2, 3)

            self.layout.addWidget(QLabel("Z"), 2, 4)
            self.layout.addWidget(self.lbl_chuck_z, 2, 5)


    def _on_chuck_x_changed(self, value: int):
        self.lbl_chuck_x.setText(str(value))

    def _on_chuck_y_changed(self, value: int):
        self.lbl_chuck_y.setText(str(value))

    def _on_chuck_z_changed(self, value: int):
        self.lbl_chuck_z.setText(str(value))

    def _on_die_no_changed(self, value: int):
        self.lbl_die_no.setText(str(value))

    def _on_structure_changed(self, value: int):
        self.lbl_structure.setText(str(value))

    def _on_die_col_changed(self, value: int):
        self.lbl_die_col.setText(str(value))

    def _on_die_row_changed(self, value: int):
        self.lbl_die_row.setText(str(value))

