from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QGroupBox, QWidget

from FlexSensor.MainWindow.view import MainThreadView
from FlexSensor.pathes import image_root


class MenuBarDefinition(QWidget):

    def __init__(self, view: MainThreadView):
        super().__init__()
        self._view = view

        # self.menubar = self.menuBar()
        self.init_menu_file()
        self.init_menu_edit()
        self.init_menu_run()
        # help_menu = menubar.addMenu("Help")
        # help_menu.addAction("About", self.on_about_clicked)



    def init_menu_file(self):
        exit_action = QAction(QIcon('exit.png'), '&Exit     ', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(lambda: exit())
        self._view._ui.menu_file.addAction(exit_action)

    def init_menu_edit(self):
        pass

    def init_menu_run(self):
        # self.menu_run = self.menubar.addMenu("Run")
        self.open_step_trough = QAction('Open &Step Through Window', self)
        self.open_step_trough.setShortcut('Ctrl+W')
        self.open_step_trough.setStatusTip('Open Step Through Window')
        self.open_step_trough.triggered.connect(self._view._on_open_step_through)
        self._view._ui.menu_run.addAction(self.open_step_trough)

        self.open_train_home_wizard = QAction('&Initial Setup Wizard', self)
        self.open_train_home_wizard.setShortcut('Ctrl+I')
        self.open_train_home_wizard.setStatusTip('Open Initial Setup Wizard')
        self.open_train_home_wizard.setIcon(QIcon(f"{image_root}/icons/setup_wizard.png"))
        self.open_train_home_wizard.triggered.connect(self._view._on_open_initial_setup_wizard)
        self._view._ui.menu_run.addAction(self.open_train_home_wizard)



