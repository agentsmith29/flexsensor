import confighandler
from LaserControl.LaserConfig import LaserConfig
from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLineEdit, QPushButton, QLabel, QDoubleSpinBox, \
    QTreeWidget

from FlexSensor.FlexSensorConfig import FlexSensorConfig


class WidgetSettingsInFilesFolders(QWidget):
    def __init__(self, config: FlexSensorConfig):
        super().__init__()
        self.config: FlexSensorConfig = config

        self.btn_select_list_of_structures = QPushButton(parent=self, text="...")
        self.btn_select_working_directory = QPushButton(parent=self, text="...")

        self.layout = QGridLayout()
        self.init_UI()

    def init_UI(self):
        grid_group_box = QGroupBox("Input Files")
        layout = QGridLayout()
        # Working directory
        layout.addWidget( self.config.output_directory.view.ui_field(), 0, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.config.wafer_config.wafermap_file.view.ui_field(), 1, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.config.wafer_config.structure_file.view.ui_field(), 2, 0)  # row, column, rowspan, colspan


        grid_group_box.setLayout(layout)
        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)


class WidgetSettingsOutFilesFolders(QWidget):
    def __init__(self, config: FlexSensorConfig):
        super().__init__()
        self.config: FlexSensorConfig = config

        self.tb_log_file = QLineEdit(
            text="self.vaut_config.wafer_config.get_log_file().filename")
        self.tb_measurement_output = QLineEdit(
            text="self.vaut_config.wafer_config.get_measurement_output().filename")
        self.tb_mat_files_output = QLineEdit(
            text="self.vaut_config.wafer_config.get_measurement_mat_file().filename")
        self.tb_bookmark_file = QLineEdit(
            text="self.vaut_config.wafer_config.get_bookmark_file()._mat_filename")
        self.tb_scope_image_file = QLineEdit(
            text="self.vaut_config.wafer_config.get_scope_image_file()._mat_filename")

        self.layout = QGridLayout()
        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()
        grid_group_box = QGroupBox("Analog Discovery 2 Settings")
        grid_group_box.setLayout(layout)
        layout.addWidget(self.config.view.widget(max_level=0), 0, 0)
        tree = QTreeWidget()

        tree.setColumnCount(3)
        tree.setHeaderLabels(["Name", "Type", "Description"])
        tree.addTopLevelItem(self.config.view.ui_tree_widget_item(tree, max_level=0))
        layout.addWidget(tree, 1, 0)

        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)

    def on_tb_scope_image_file_text_changed(self, value):
        return
        # if value is not None:
        #     self.config.wafer_config.get_scope_image_file().set_obj(value)
        # val = self.config.wafer_config.get_scope_image_file().relative.replace(self.config.get_output_directory().relative,
        #                                                                  "<b>wd</b>")
        # self.lbl_scope_image_file.setText(val)
        # # set label hover text
        # self.lbl_scope_image_file.setToolTip(self.config.wafer_config.get_scope_image_file().absolute)

    def on_tb_measurement_output_text_changed(self, value):
        return
        # if value is not None:
        #     self.config.wafer_config.measurement_output.set(value)
        # val = self.config.wafer_config.measurement_output.get().replace(self.config.output_directory.get(),
        #                                                                    "<b>wd</b>")
        # self.lbl_measurement_output.setText(val)
        # # set label hover text
        # self.lbl_measurement_output.setToolTip(self.config.wafer_config.scope_image_file.get())

    def on_tb_bookmark_file_text_changed(self, value):
        return
        # if value is not None:
        #     self.config.wafer_config.get_bookmark_file().set_obj(value)
        # val = self.config.wafer_config.get_bookmark_file().relative.replace(self.config.get_output_directory().relative,
        #                                                               "<b>wd</b>")
        # self.lbl_bookmark_file.setText(val)
        # # set label hover text
        # self.lbl_bookmark_file.setToolTip(self.config.wafer_config.get_bookmark_file().absolute)
        #
        # config = self.config

    def on_tb_mat_files_output_text_changed(self, value):
        return
        # if value is not None:
        #     self.config.wafer_config.measurement_mat_file.set(value)
        # val = self.config.wafer_config.measurement_mat_file.get().replace(
        #     self.config.output_directory.get().relative,"<b>wd</b>")
        # self.lbl_mat_files_output.setText(val)
        # self.lbl_mat_files_output.setToolTip(self.config.wafer_config.measurement_mat_file.absolute)

    def on_tb_log_file_text_changed(self, value):
        return
        #if value is not None:
        #    self.config.wafer_config.log_file.set(value)
        #
        #val = self.config.wafer_config.log_file.get().replace(self.config.output_directory.get(), "<b>wd</b>")
        #self.lbl_log_file.setText(val)
        #self.lbl_log_file.setToolTip(self.config.wafer_config.log_file.get())


class WidgetAD2Settings(QWidget):
    def __init__(self, config: FlexSensorConfig):
        super().__init__()
        self.tb_ad2_raw_out_file = QLineEdit()
        self.config = config
        # self.c = #ConfigView(vaut_config)

        self.num_sample_rate = QDoubleSpinBox()
        self.num_total_samples = QDoubleSpinBox()
        self.num_sample_time = QDoubleSpinBox()

        self.btn_select_ad2_raw_out_file = QPushButton(parent=self, text="....")

        self.btn_select_ad2_raw_out_file.clicked.connect(self.show_config)
        self.layout = QGridLayout()
        self.init_UI()

    def show_config(self):
        pass
        # self.c = ConfigView(self.vaut_config)
        # self.c.show()

    def init_UI(self):
        layout = QGridLayout()
        grid_group_box = QGroupBox("Analog Discovery 2 Settings")
        grid_group_box.setLayout(layout)
        layout.addWidget(self.config.view.widget(), 0, 0)
        tree = QTreeWidget()

        tree.setColumnCount(3)
        tree.setHeaderLabels(["Name", "Type", "Description"])
        tree.addTopLevelItem(self.config.view.ui_tree_widget_item(tree))
        layout.addWidget(tree, 1, 0)

        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)


class WidgetLaserSettings(QWidget):
    def __init__(self, laser_config: LaserConfig):
        super().__init__()
        self.config = laser_config
        self.c = None

        self.num_wavelength_sweep_start = QDoubleSpinBox()
        self.num_wavelength_range_stop = QDoubleSpinBox()
        self.num_velocity = QDoubleSpinBox()
        self.num_acceleration = QDoubleSpinBox()
        self.num_deceleration = QDoubleSpinBox()

        # self.btn_select_ad2_raw_out_file = QPushButton(parent=self, text="....")

        # self.btn_select_ad2_raw_out_file.clicked.connect(self.show_config)
        self.layout = QGridLayout()
        self.init_UI()

    def show_config(self):
        pass
        #self.c = ConfigView(self.vaut_config)
        #self.c.show()

    def init_UI(self):
        layout = QGridLayout()
        grid_group_box = QGroupBox("Laser Settings")
        grid_group_box.setLayout(layout)
        layout.addWidget(self.config.view.widget(), 0, 0)
        tree = QTreeWidget()

        tree.setColumnCount(3)
        tree.setHeaderLabels(["Name", "Type", "Description"])
        tree.addTopLevelItem(self.config.view.ui_tree_widget_item(tree))
        layout.addWidget(tree, 1, 0)

        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)
