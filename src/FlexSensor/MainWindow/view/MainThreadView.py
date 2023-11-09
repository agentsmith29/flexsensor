import logging
import sys
import traceback

from PySide6.QtWidgets import (
    QMessageBox, QGridLayout, QGroupBox, QStatusBar, QPushButton, QTabWidget, QToolButton, QDockWidget, )
from PySide6.QtCore import QThread

from PySide6.QtGui import QIcon, QAction

import pyqtgraph as pg
from pyqtgraph.dockarea import *

import __version__
from ConfigHandler.controller.VASInputFileParser import VASInputFileParser
from MainWindow.view.BaseWindow import BaseWindow
from MainWindow.view.widgets.HomeStatusWidget import HomeStatusWidget
from MainWindow.view.widgets.ScopeWidget import ScopeWidget

from MainWindow.view.MainView import Ui_MainWindow

from MainWindow.controller.MainThreadController import MainThreadController
from MainWindow.model.MainThreadModel import MainThreadModel
from MainWindow.view.StepThroughView import StepThroughView
from InitialSetupWizard.InitialSetupWizard import InitialSetupWizard
from MainWindow.view.widgets.WidgetSettingsFilesFolders import (WidgetSettingsOutFilesFolders,
                                                                WidgetLaserSettings, WidgetSettingsInFilesFolders,
                                                                WidgetAD2Settings)
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData
from MeasurementEvaluationTool.view.widgets.MenuBarDefinition import MenuBarDefinition
from constants.qs_style_sheets import CSSPlayPushButton

#
from pathes import image_root
import ConfigHandler as Config


class MainWindow(BaseWindow):

    def __init__(self, model: MainThreadModel, controller: MainThreadController):
        super().__init__(Ui_MainWindow())
        self.logger = logging.getLogger("MainThread (UI)")

        self._model: MainThreadModel = model
        self._controller: MainThreadController = controller

        # Signals for finished acquisition
        self.model.measurement_routine.signals.routine_iteration_finished.connect(
            self.on_routine_iteration_finished)

        self._ui.settingsTopBtn.clicked.connect(self.openCloseRightBox)
        self._ui.toggleButton.clicked.connect(lambda: self.toggleMenu(True))
        self._ui.btn_start_measuring_routine.clicked.connect(self._on_btn_run_clicked)

        self.init_UI()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        self._ui.stackedWidget.setCurrentWidget(self._ui.home)
        self._ui.btn_home.setStyleSheet(self.selectMenu(self._ui.btn_home.styleSheet()))

    @property
    def model(self) -> MainThreadModel:
        return self._model

    @property
    def controller(self) -> MainThreadController:
        return self._controller

    # ==================================================================================================================
    # UI initialization methods
    # ==================================================================================================================
    def init_UI(self):
        self.logger.debug("Initializing UI of MainWindow.")
        self.grid_layout_main = QGridLayout()
        self.init_UI_status_bar()
        self.menu_bar = MenuBarDefinition(self)

        # Add the prober control
        self._ui.prober_control_layout.addWidget(self.model.prober_window)
        self._ui.btn_probe_control.clicked.connect(self._on_btn_prober_control_clicked)

        # Add the ADC control
        dock_ad2 = QDockWidget("AD2 Control", self)
        dock_ad2.setWidget(self.model.ad2_window)
        self._ui.adc_control_layout.addWidget(dock_ad2, 0,0)
        self._ui.btn_adc_control.clicked.connect(self._on_btn_adc_control_clicked)

        dock_laser = QDockWidget("Laser Control", self)
        dock_laser.setWidget(self.model.laser_window)
        self._ui.adc_control_layout.addWidget(dock_laser,0,1)
        self._ui.btn_laser_control.clicked.connect(self._on_btn_laser_control_clicked)

        # add the measurement evaluation tool
        self._ui.measured_data_layout.addWidget(self.model.mea_eval_tool_window)
        self._ui.btn_measured_data.clicked.connect(self._on_btn_measurement_evaluation_clicked)


        self._ui.home_layout.addWidget(HomeStatusWidget(self), 0, 0, 1, 2)
        self._ui.home_layout.addWidget(self.init_UI_measurement_settings(), 1, 0)
        self._ui.home_layout.addWidget(ScopeWidget(self), 1, 1)
        # self._ui.grid_layout_main.addWidget(self.init_UI_device_control(), 1, 1, 2, 1)

        self._ui.home_layout.addWidget(self.init_UI_buttons(), 2, 0, 1, 2)
        self._ui.btn_home.clicked.connect(self._on_btn_home_clicked)

        # self.setGeometry(100, 100, 1250, 150)
        self.setWindowTitle(f'FlexSensor Automator {__version__.__version__}')
        self.setWindowIcon(QIcon('../images/FlexSensorIcon.png'))

        # self.init_menu_run()

        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        self._ui.closeAppBtn.clicked.connect(lambda: exit())


    # def closeEvent(self, *args, **kwargs):
    #     # self.prober_worker.stop()
    #     # self.threadpool.waitForDone()
    #     self.thread.quit()
    #     self.logger.warning(f"Exiting {args}")
    #     sys.exit(1)

    def init_UI_status_bar(self):
        # global status_bar

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def init_UI_measurement_settings(self):
        tabwidget = QTabWidget()
        self.configView = Config.View(self.model.vaut_config)
        tab_input = tabwidget.addTab(WidgetSettingsInFilesFolders(self.model.vaut_config), "Input")
        tab_folders = tabwidget.addTab(WidgetSettingsOutFilesFolders(self.model.vaut_config), "Folder Settings")
        tab_ad2 = tabwidget.addTab(WidgetAD2Settings(self.model.vaut_config), "AD2 Settings")
        tab_laser = tabwidget.addTab(WidgetLaserSettings(self.model.vaut_config), "Laser Settings")
        tab_yaml = tabwidget.addTab(self.configView, "YAML Config")
        tabwidget.currentChanged.connect(
            lambda idx: self.configView.repopulate(self.model.vaut_config) if idx == tab_yaml else print("fg")
        )
        return tabwidget

    # def init_UI_device_control(self):
    #     tabwidget = QTabWidget()
    #     # tab_scope = tabwidget.addTab(self.init_scope_meter(), "Scope")
    #     # tab_laser = tabwidget.addTab(self._controller.laser_window, "Laser Control")
    #     # tab_ad2dev = tabwidget.addTab(self._controller.ad2_window, "AD2 Control")
    #     # tab_prober = tabwidget.addTab(self._controller.prober_window, "Prober Control")
    #
    #     return tabwidget

    def init_scope_meter(self):
        area = DockArea()

        d1 = Dock("Analog Discovery 2")
        d2 = Dock("Filtered")
        area.addDock(d1, 'bottom')
        area.addDock(d2, 'bottom', d1)

        self.scope_original = pg.PlotWidget(title="AD2 Acquisition")
        # self.scope_original.plot(np.random.normal(size=100)*1e12)
        self.scope_original.plotItem.showGrid(x=True, y=True, alpha=1)
        d1.addWidget(self.scope_original)

        self.scope_filtered = pg.PlotWidget(title="Filtered Data")
        # self.scope_filtered.plot(np.random.normal(size=100))
        self.scope_filtered.plotItem.showGrid(x=True, y=True, alpha=1)
        d2.addWidget(self.scope_filtered)

        # self.scope = pg.PlotWidget()
        # self.scope.plot([1, 2])

        return area

    def init_UI_buttons(self):
        grid_group_box = QGroupBox()
        layout = QGridLayout()

        self.btn_run = QPushButton(parent=self, text="Run")
        self.btn_run.clicked.connect(self._on_btn_run_clicked)
        layout.addWidget(self.btn_run, 0, 0)

        self.btn_stop = QPushButton(parent=self, text="Stop")
        # self.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        layout.addWidget(self.btn_stop, 0, 1)

        self.btn_exit = QPushButton(parent=self, text="Exit")
        # self.btn_exit.clicked.connect(self.on_btn_exit_clicked)
        layout.addWidget(self.btn_exit, 0, 2)

        grid_group_box.setLayout(layout)

        return grid_group_box

    # def init_menu_file(self):
    #     exit_action = QAction(QIcon('exit.png'), '&Exit     ', self)
    #     exit_action.setShortcut('Ctrl+Q')
    #     exit_action.setStatusTip('Exit application')
    #     exit_action.triggered.connect(self.close)
    #     self._ui.menu_file.addAction(exit_action)
    #
    # def init_menu_edit(self):
    #     pass
    #
    # def init_menu_run(self):
    #     # self.menu_run = self.menubar.addMenu("Run")
    #     self.open_step_trough = QAction('Open &Step Through Window', self)
    #     self.open_step_trough.setShortcut('Ctrl+W')
    #     self.open_step_trough.setStatusTip('Open Step Through Window')
    #     self.open_step_trough.triggered.connect(self.on_open_step_through)
    #     self._ui.menu_run.addAction(self.open_step_trough)
    #
    #     self.open_train_home_wizard = QAction('&Initial Setup Wizard', self)
    #     self.open_train_home_wizard.setShortcut('Ctrl+I')
    #     self.open_train_home_wizard.setStatusTip('Open Initial Setup Wizard')
    #     self.open_train_home_wizard.setIcon(QIcon(f"{image_root}/icons/setup_wizard.png"))
    #     self.open_train_home_wizard.triggered.connect(self.on_open_initial_setup_wizard)
    #     self._ui.menu_run.addAction(self.open_train_home_wizard)
    #
    #
    # def init_UI_menu_bar(self):
    #     # self.menubar = self.menuBar()
    #     self.init_menu_file()
    #     self.init_menu_edit()
    #     self.init_menu_run()
    #     # help_menu = menubar.addMenu("Help")
    #     # help_menu.addAction("About", self.on_about_clicked)

    # ==================================================================================================================
    # Signal handlers
    # ==================================================================================================================
    def _on_open_step_through(self):
        file_parser = VASInputFileParser()
        grouped_structures, _ = file_parser.read_file(
            input_file=self.model.vaut_config.wafer_config.get_structure_file().absolute
        )
        self.step_through_view = StepThroughView(grouped_structures)
        self.step_through_view.show()

    def _on_open_initial_setup_wizard(self):
        self.wizard = InitialSetupWizard(self.model.prober_controller)
        self.wizard.show()

    def _on_btn_laser_control_clicked(self):
        self.resetStyle(self.sender().objectName())
        self._ui.stackedWidget.setCurrentWidget(self._ui.laser_control)
        self.sender().setStyleSheet(self.selectMenu(self.sender().styleSheet()))

    def _on_btn_adc_control_clicked(self):
        self.resetStyle(self.sender().objectName())
        self._ui.stackedWidget.setCurrentWidget(self._ui.adc_control)
        self.sender().setStyleSheet(self.selectMenu(self.sender().styleSheet()))

    def _on_btn_prober_control_clicked(self):
        self.resetStyle(self.sender().objectName())
        self._ui.stackedWidget.setCurrentWidget(self._ui.prober_control)
        self.sender().setStyleSheet(self.selectMenu(self.sender().styleSheet()))

    def _on_btn_home_clicked(self):
        self.resetStyle(self.sender().objectName())
        self._ui.stackedWidget.setCurrentWidget(self._ui.home)
        self.sender().setStyleSheet(self.selectMenu(self.sender().styleSheet()))

    def _on_btn_measurement_evaluation_clicked(self):
        self.resetStyle(self.sender().objectName())
        self._ui.stackedWidget.setCurrentWidget(self._ui.measured_data)
        self.sender().setStyleSheet(self.selectMenu(self.sender().styleSheet()))

    def _on_btn_run_clicked(self):
        self._ui.btn_start_measuring_routine.setStyleSheet(CSSPlayPushButton.style_pause())
        self._controller.start_measurement_routine()

    # ------------------------------------------------------------------------------------------------------------------
    # not used (yet)
    def on_wafer_version_changed(self, value):
        pass
        # # Set the object property
        # self.vaut_config.set_wafer_version(value)
        # # Update all textfields
        # self.on_tb_log_file_text_changed(self.tb_log_file.text())
        # self.on_tb_bookmark_file_text_changed(self.tb_bookmark_file.text())
        # self.on_tb_scope_image_file_text_changed(self.tb_scope_image_file.text())
        # self.on_tb_mat_files_output_text_changed(self.tb_mat_files_output.text())
        # self.on_tb_measurement_output_text_changed(self.tb_measurement_output.text())
        # self.tb_working_directory.setText(self.vaut_config.output_directory.rel)

    def on_wafer_nr_changed(self, value):
        pass
        # # Set the object property
        # self.vaut_config.set_wafer_nr(value)
        # # Update all textfields
        # self.on_tb_log_file_text_changed(self.tb_log_file.text())
        # self.on_tb_bookmark_file_text_changed(self.tb_bookmark_file.text())
        # self.on_tb_scope_image_file_text_changed(self.tb_scope_image_file.text())
        # self.on_tb_mat_files_output_text_changed(self.tb_mat_files_output.text())
        # self.on_tb_measurement_output_text_changed(self.tb_measurement_output.text())
        # self.tb_working_directory.setText(self.vaut_config.output_directory.rel)

    def on_routine_iteration_finished(self, cur_measured_signal: SingleMeasuredData = None):
        pass
        # if not isinstance(cur_measured_signal, SingleMeasuredData):
        #     self.logger.error(
        #         f"Prober did not return any valid measured signal: measured_signal was {type(cur_measured_signal)}")
        #     self.on_error_emitted((ValueError,
        #                            f"Prober did not return any valid measured signal: measured_signal was {type(cur_measured_signal)}",
        #                            traceback.format_exc()))
        #     # raise ValueError(f"Prober did not return any valid measured signal: measured_signal was {type(measured_signal)}")

        # self.logger.info(
        #     f"Acquisition finished for structure {cur_measured_signal.wafer_properties.structure_name} (die: {cur_measured_signal.wafer_properties.die_number}).")
        # try:
        #     if len(cur_measured_signal._filtered_amplitude['amplitude']) > 0:
        #         self.scope_original.clear()
        #         self.scope_original.plot(cur_measured_signal.measured_data['measurements'], pen=pg.mkPen(width=1))
        #     else:
        #         self.logger.warning("Nothing to plot!")
        # except Exception as e:
        #     self.logger.error(f"Error plotting scope: {e}")
        #     self.on_error_emitted((type(e), f"Error plotting scope: {e}", traceback.format_exc()))

    def on_error(self, error_message):
        self.logger.error(error_message)
        self.status_bar.showMessage(error_message)
        self.status_bar.setStyleSheet("color: red")

    def on_writeout_emitted(self, msg_type, message):

        if msg_type == "debug":
            self.status_bar.setStyleSheet('border: 0; color:  blue;')
        elif msg_type == "warning":
            self.status_bar.setStyleSheet('border: 0; color:  orange;')
        elif msg_type == "error":
            self.status_bar.setStyleSheet('border: 0; color:  red;')
        elif msg_type == "fatal":
            self.status_bar.setStyleSheet('border: 0; color:  red;')
        else:
            self.status_bar.setStyleSheet('border: 0; color:  black;')
        self.status_bar.showMessage(message)

    def on_report_info_emitted(self, version_info):
        self.lbl_die_no.setText("<b>" + str(version_info["die_no"]) + "</b>")
        self.lbl_structure.setText("<b>" + str(version_info["structure"]) + "</b>")
        self.lbl_die_col.setText("<b>" + str(version_info["chuck_col"]) + "</b>")
        self.lbl_die_row.setText("<b>" + str(version_info["chuck_row"]) + "</b>")

    def on_report_progress(self, progress):
        self.progress.setValue(progress)

    def on_structure_select(self):
        pass
        # self.test_win.show()

    def on_error_emitted(self, value):
        title, text, details = value
        try:
            self.error_dialog: QMessageBox
            # self.error_dialog.close()
        except Exception as e:
            print(f"Can't close error_dialog: {e}")
        # Show a error dialog
        self.error_dialog = QMessageBox()
        self.error_dialog.setText(str(text))
        # set detailed text
        self.error_dialog.setDetailedText(str(details))
        self.error_dialog.setIcon(QMessageBox.Critical)
        self.error_dialog.setWindowTitle(f"Measurmenent Routine Error: {title}")
        self.error_dialog.exec_()

    def on_warning_emitted(self, value):
        try:
            self.warning_dialog: QMessageBox
            self.warning_dialog.close()
        except Exception as e:
            print(f"Can't close warning_dialog: {e}")

        # Show a warning dialog
        self.warning_dialog = QMessageBox()
        self.warning_dialog.setText(str(value[1]))
        # set detailed text
        self.warning_dialog.setDetailedText(str(value[2]))
        self.warning_dialog.setIcon(QMessageBox.Warning)
        self.warning_dialog.setWindowTitle(f"Prober Task Warning: {value[0]}")
        self.warning_dialog.exec_()

    def closeEvent(self, event):
        # do stuff
        self.model.ad2_controller.stop_process()
        self.model.laser_controller.stop_process()
        event.accept() # let the window close


    def __del__(self):
        self.logger.info("Exiting")
        quit()