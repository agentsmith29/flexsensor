from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLineEdit, QPushButton, QLabel, QDoubleSpinBox

from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
from ConfigHandler.view.ConfigView import ConfigView


class WidgetSettingsInFilesFolders(QWidget):
    def __init__(self, vaut_config: VAutomatorConfig):
        super().__init__()
        self.vaut_config = vaut_config

        self.btn_select_list_of_structures = QPushButton(parent=self, text="...")
        self.btn_select_working_directory = QPushButton(parent=self, text="...")

        self.layout = QGridLayout()
        self.init_UI()

    def init_UI(self):
        grid_group_box = QGroupBox("Input Files")
        layout = QGridLayout()
        # Working directory
        self.tb_working_directory = QLineEdit(parent=self, text=str(self.vaut_config.get_output_directory().relative))
        self.btn_select_working_directory.setMaximumWidth(self.btn_select_working_directory.sizeHint().height())
        layout.addWidget(QLabel("Working directory"), 0, 0)
        layout.addWidget(self.tb_working_directory, 0, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.btn_select_working_directory, 0, 3)  # row, column, rowspan, colspan

        # List of structures
        self.tb_list_of_structures = QLineEdit(parent=self, text=str(self.vaut_config.wafer_config.get_structure_file().relative))
        self.btn_select_list_of_structures.setMaximumWidth(self.btn_select_list_of_structures.sizeHint().height())
        layout.addWidget(QLabel("Input Structure File"), 1, 0)
        layout.addWidget(self.tb_list_of_structures, 1, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.btn_select_list_of_structures, 1, 3)  # row, column, rowspan, colspan

        grid_group_box.setLayout(layout)
        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)


class WidgetSettingsOutFilesFolders(QWidget):
    def __init__(self, vaut_config: VAutomatorConfig):
        super().__init__()
        self.vaut_config = vaut_config

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
        grid_group_box = QGroupBox("Output Files")
        grid_group_box.setLayout(layout)






        self.lbl_log_file = QLabel(parent=self)
        self.tb_log_file.textChanged.connect(self.on_tb_log_file_text_changed)
        self.on_tb_log_file_text_changed(self.tb_log_file.text())
        layout.addWidget(QLabel("Log File"), 0, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_log_file, 0, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.lbl_log_file, 1, 0, 1, 2)  # row, column, rowspan, colspan

        # measurement output
        self.lbl_measurement_output = QLabel(parent=self)
        self.tb_measurement_output.textChanged.connect(self.on_tb_measurement_output_text_changed)
        self.on_tb_measurement_output_text_changed(self.tb_measurement_output.text())
        layout.addWidget(QLabel("Measurement output"), 2, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_measurement_output, 2, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.lbl_measurement_output, 3, 0, 1, 2)  # row, column, rowspan, colspan

        # Mat files output
        self.lbl_mat_files_output = QLabel(parent=self)
        self.on_tb_mat_files_output_text_changed(self.tb_mat_files_output.text())

        self.tb_mat_files_output.textChanged.connect(self.on_tb_mat_files_output_text_changed)
        layout.addWidget(QLabel("Matlab Files"), 4, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_mat_files_output, 4, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.lbl_mat_files_output, 5, 0, 1, 2)  # row, column, rowspan, colspan

        # bookmark files
        self.lbl_bookmark_file = QLabel(parent=self)
        self.on_tb_bookmark_file_text_changed(self.tb_bookmark_file.text())
        self.tb_bookmark_file.textChanged.connect(self.on_tb_bookmark_file_text_changed)
        self.tb_scope_image_file.textChanged.connect(self.on_tb_scope_image_file_text_changed)
        layout.addWidget(QLabel("Bookmark files"), 6, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_bookmark_file, 6, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.lbl_bookmark_file, 7, 0, 1, 2)  # row, column, rowspan, colspan

        # scope shots
        self.lbl_scope_image_file = QLabel(parent=self)
        self.on_tb_scope_image_file_text_changed(self.tb_scope_image_file.text())
        layout.addWidget(QLabel("Scope Shots"), 8, 0)  # row, column, rowspan, colspan
        layout.addWidget(self.tb_scope_image_file, 8, 1)  # row, column, rowspan, colspan
        layout.addWidget(self.lbl_scope_image_file, 9, 0, 1, 2)


        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)

    def on_tb_scope_image_file_text_changed(self, value):
        if value is not None:
            self.vaut_config.wafer_config.get_scope_image_file().set_obj(value)
        val = self.vaut_config.wafer_config.get_scope_image_file().relative.replace(self.vaut_config.get_output_directory().relative,
                                                                         "<b>wd</b>")
        self.lbl_scope_image_file.setText(val)
        # set label hover text
        self.lbl_scope_image_file.setToolTip(self.vaut_config.wafer_config.get_scope_image_file().absolute)

    def on_tb_measurement_output_text_changed(self, value):
        if value is not None:
            self.vaut_config.wafer_config.get_measurement_output().set_obj(value)
        val = self.vaut_config.wafer_config.get_measurement_output().relative.replace(self.vaut_config.get_output_directory().relative,
                                                                           "<b>wd</b>")
        self.lbl_measurement_output.setText(val)
        # set label hover text
        self.lbl_measurement_output.setToolTip(self.vaut_config.wafer_config.get_scope_image_file().absolute)

    def on_tb_bookmark_file_text_changed(self, value):
        if value is not None:
            self.vaut_config.wafer_config.get_bookmark_file().set_obj(value)
        val = self.vaut_config.wafer_config.get_bookmark_file().relative.replace(self.vaut_config.get_output_directory().relative,
                                                                      "<b>wd</b>")
        self.lbl_bookmark_file.setText(val)
        # set label hover text
        self.lbl_bookmark_file.setToolTip(self.vaut_config.wafer_config.get_bookmark_file().absolute)

        config = self.vaut_config

    def on_tb_mat_files_output_text_changed(self, value):
        if value is not None:
            self.vaut_config.wafer_config.get_measurement_mat_file().set_obj(value)
        val = self.vaut_config.wafer_config.get_measurement_mat_file().relative.replace(
            self.vaut_config.get_output_directory().relative,
                                                                             "<b>wd</b>")
        self.lbl_mat_files_output.setText(val)
        self.lbl_mat_files_output.setToolTip(self.vaut_config.wafer_config.get_measurement_mat_file().absolute)

    def on_tb_log_file_text_changed(self, value):
        if value is not None:
            self.vaut_config.wafer_config.get_log_file().set_obj(value)

        val = self.vaut_config.wafer_config.get_log_file().relative.replace(self.vaut_config.get_output_directory().relative, "<b>wd</b>")
        self.lbl_log_file.setText(val)
        self.lbl_log_file.setToolTip(self.vaut_config.wafer_config.get_log_file().absolute)

class WidgetAD2Settings(QWidget):
    def __init__(self, vaut_config: VAutomatorConfig):
        super().__init__()
        self.vaut_config = vaut_config
        self.c = ConfigView(vaut_config)


        self.num_sample_rate = QDoubleSpinBox()
        self.num_total_samples = QDoubleSpinBox()
        self.num_sample_time = QDoubleSpinBox()

        self.btn_select_ad2_raw_out_file = QPushButton(parent=self, text="....")

        self.btn_select_ad2_raw_out_file.clicked.connect(self.show_config)
        self.layout = QGridLayout()
        self.init_UI()


    def show_config(self):
        self.c = ConfigView(self.vaut_config)
        self.c.show()

    def init_UI(self):
        layout = QGridLayout()
        grid_group_box = QGroupBox("Analog Discovery 2 Settings")
        grid_group_box.setLayout(layout)

        lbl_sample_rate = QLabel("Sample Rate")
        layout.addWidget(lbl_sample_rate, 1, 0)
        self.num_sample_rate.valueChanged.connect(lambda v: self.vaut_config.ad2_device_config.set_sample_rate(v))
        self.num_sample_rate.setRange(0, 10**8)
        self.num_sample_rate.setSingleStep(1)
        self.num_sample_rate.setValue(self.vaut_config.ad2_device_config.get_sample_rate())
        self.num_sample_rate.setSuffix(" Hz")
        self.num_sample_rate.setDecimals(3)
        self.num_sample_rate.setKeyboardTracking(False)
        layout.addWidget(self.num_sample_rate, 1, 1, 1, 2)

        lbl_total_samples = QLabel("Total Samples")
        layout.addWidget(lbl_total_samples, 2, 0)
        self.num_total_samples.setRange(0, 10**8)
        self.num_total_samples.setSingleStep(1)
        self.num_total_samples.setValue(self.vaut_config.ad2_device_config.get_total_samples())
        self.num_total_samples.setDecimals(3)
        self.num_total_samples.setKeyboardTracking(False)
        layout.addWidget(self.num_total_samples, 2, 1, 1, 2)

        lbl_sample_time = QLabel("Sample Time")
        layout.addWidget(lbl_sample_time, 3, 0)
        self.num_sample_time.setRange(0, 10**8)
        self.num_sample_time.setSingleStep(1)
        self.num_sample_time.setValue(self.vaut_config.ad2_device_config.get_sample_time())
        self.num_sample_time.setSuffix(" s")
        self.num_sample_time.setDecimals(3)
        self.num_sample_time.setKeyboardTracking(False)
        layout.addWidget(self.num_sample_time, 3, 1, 1, 2)

        lbl_ad2_raw_out_file = QLabel("Raw Out File")
        layout.addWidget(lbl_ad2_raw_out_file, 4, 0)
        tb_ad2_raw_out_file = QLineEdit(text=self.vaut_config.ad2_device_config.get_ad2_raw_out_file().relative)
        layout.addWidget(tb_ad2_raw_out_file, 4, 1)
        layout.addWidget(self.btn_select_ad2_raw_out_file, 4, 2)

        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)

class WidgetLaserSettings(QWidget):
    def __init__(self, vaut_config: VAutomatorConfig):
        super().__init__()
        self.vaut_config = vaut_config
        self.c = None


        self.num_wavelength_sweep_start = QDoubleSpinBox()
        self.num_wavelength_range_stop = QDoubleSpinBox()
        self.num_velocity = QDoubleSpinBox()
        self.num_acceleration = QDoubleSpinBox()
        self.num_deceleration = QDoubleSpinBox()


        #self.btn_select_ad2_raw_out_file = QPushButton(parent=self, text="....")

        #self.btn_select_ad2_raw_out_file.clicked.connect(self.show_config)
        self.layout = QGridLayout()
        self.init_UI()


    def show_config(self):
        self.c = ConfigView(self.vaut_config)
        self.c.show()

    def init_UI(self):
        layout = QGridLayout()
        grid_group_box = QGroupBox("Laser Settings")
        grid_group_box.setLayout(layout)

        lbl_wavelength_sweep_start = QLabel("Wavelength Sweep")
        layout.addWidget(lbl_wavelength_sweep_start, 1, 0)



        self.num_wavelength_sweep_start.setRange(0, 10 ** 8)
        self.num_wavelength_sweep_start.setSingleStep(1)
        self.num_wavelength_sweep_start.setValue(self.vaut_config.laser_config.get_wavelength_range()[0])
        self.num_wavelength_sweep_start.setSuffix(" nm")
        self.num_wavelength_sweep_start.setDecimals(3)
        self.num_wavelength_sweep_start.setKeyboardTracking(False)
        layout.addWidget(self.num_wavelength_sweep_start, 1, 1)
        self.num_wavelength_sweep_start.valueChanged.connect(
            lambda v: self.vaut_config.laser_config.set_wavelength_range(
                [float(v), float(self.num_wavelength_range_stop.value())])
        )

        self.num_wavelength_range_stop.setRange(0, 10 ** 8)
        self.num_wavelength_range_stop.setSingleStep(1)
        self.num_wavelength_range_stop.setValue(self.vaut_config.laser_config.get_wavelength_range()[1])
        self.num_wavelength_range_stop.setSuffix(" nm")
        self.num_wavelength_range_stop.setDecimals(3)
        self.num_wavelength_range_stop.setKeyboardTracking(False)
        layout.addWidget(self.num_wavelength_range_stop, 1, 2)

        self.num_wavelength_range_stop.valueChanged.connect(
            lambda v: self.vaut_config.laser_config.set_wavelength_range(
                [float(self.num_wavelength_sweep_start.value()), float(v)]
        ))

        lbl_velocity = QLabel("Velocity")
        layout.addWidget(lbl_velocity, 2, 0)
        self.num_velocity.valueChanged.connect(lambda v: self.vaut_config.laser_config.set_velocity(v))
        self.num_velocity.setRange(0, 10**8)
        self.num_velocity.setSingleStep(1)
        self.num_velocity.setValue(self.vaut_config.laser_config.get_velocity())
        self.num_acceleration.setSuffix(" m/s")
        self.num_velocity.setDecimals(3)
        self.num_velocity.setKeyboardTracking(False)
        layout.addWidget(self.num_velocity, 2, 1, 1, 2)

        lbl_acceleration = QLabel("Acceleration")
        layout.addWidget(lbl_acceleration, 3, 0)
        self.num_acceleration.valueChanged.connect(lambda v: self.vaut_config.laser_config.set_acceleration(v))
        self.num_acceleration.setRange(0, 10**8)
        self.num_acceleration.setSingleStep(1)
        self.num_acceleration.setValue(self.vaut_config.laser_config.get_acceleration())
        self.num_acceleration.setSuffix(" m/s^2")
        self.num_acceleration.setDecimals(3)
        self.num_acceleration.setKeyboardTracking(False)
        layout.addWidget(self.num_acceleration, 3, 1, 1, 2)

        lbl_deceleration = QLabel("Deceleration")
        layout.addWidget(lbl_deceleration, 4, 0)
        self.num_deceleration.valueChanged.connect(lambda v: self.vaut_config.laser_config.set_deceleration(v))
        self.num_deceleration.setRange(0, 10 ** 8)
        self.num_deceleration.setSingleStep(1)
        self.num_deceleration.setValue(self.vaut_config.laser_config.get_deceleration())
        self.num_deceleration.setSuffix(" m/s^2")
        self.num_deceleration.setDecimals(3)
        self.num_deceleration.setKeyboardTracking(False)
        layout.addWidget(self.num_deceleration, 4, 1, 1, 2)


        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)

