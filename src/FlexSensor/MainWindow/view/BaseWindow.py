from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtGui import QColor, Qt, QIcon
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QSizeGrip, QPushButton

import __version__

from MainWindow.view.MainView import Ui_MainWindow
from MainWindow.view.widgets.custom_grips import CustomGrip

from FlexSensor.FlexSensorConfig import FlexSensorConfig


class BaseWindow(QMainWindow):

    def __init__(self, ui_main_window: Ui_MainWindow, config: FlexSensorConfig):
        super().__init__()
        self.GLOBAL_STATE = False
        self.GLOBAL_TITLE_BAR = True

        self._ui = ui_main_window
        self._ui.setupUi(self)
        self.app_config = config.app_config
        self.app_config.ENABLE_CUSTOM_TITLE_BAR.set(True)

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "FlexSensor 6 - A SiPh automation tool"
        description = f"Flexsensor  {__version__.__version__}"
        # APPLY TEXTS
        self.setWindowTitle(title)
        self._ui.titleRight.setText(description)

        if not self.app_config.ENABLE_CUSTOM_TITLE_BAR.get():
            self._ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self._ui.minimizeAppBtn.hide()
            self._ui.maximizeRestoreAppBtn.hide()
            self._ui.closeAppBtn.hide()
            self._ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self._ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self._ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        # self.setStyleSheet("background-color: rgb(0, 0, 0);")

        # MINIMIZE
        self._ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self._ui.maximizeRestoreAppBtn.clicked.connect(lambda: self.maximize_restore())

        # CLOSE APPLICATION
        self._ui.closeAppBtn.clicked.connect(lambda: self.close())

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)
        self.maximize_restore()
        # self._ui.titleRightInfo.mouseMoveEvent = self.moveWindow

    # def moveWindow(self, event):

    def openCloseRightBox(self):
        self.toggleRightBox(True)

    def openCloseLeftBox(self):
        self.toggleLeftBox(True)

    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self._ui.extraLeftBox.width()
            widthRightBox = self._ui.extraRightBox.width()
            maxExtend = self.app_config.LEFT_BOX_WIDTH.get()
            color = self.app_config.BTN_LEFT_BOX_COLOR.get()
            standard = 0

            # GET BTN STYLE
            style = self._ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self._ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self._ui.settingsTopBtn.styleSheet()
                    self._ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self._ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))

        self.start_box_animation(width, widthRightBox, "left")

    # UI initialization
    # TOGGLE RIGHT BOX
    #     # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH
            width = self._ui.extraRightBox.width()
            widthLeftBox = self._ui.extraLeftBox.width()
            maxExtend = self.app_config.RIGHT_BOX_WIDTH.get()
            color = self.app_config.BTN_RIGHT_BOX_COLOR.get()
            standard = 0

            # GET BTN STYLE
            style = self._ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self._ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self._ui.toggleLeftBox.styleSheet()
                    self._ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self._ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            self.start_box_animation(widthLeftBox, width, "right")

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH
            width = self._ui.leftMenuBg.width()
            maxExtend = self.app_config.MENU_WIDTH.get()
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self._ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0

            # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self._ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(self._ui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(self.app_config.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def selectMenu(self, getStyle):
        select = getStyle + self.app_config.MENU_SELECTED_STYLESHEET.get()
        return select

    def deselectMenu(self, getStyle):
        deselect = getStyle.replace(self.app_config.MENU_SELECTED_STYLESHEET.get(), "")
        return deselect

    # START SELECTION
    def selectStandardMenu(self, widget):
        for w in self._ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(self.selectMenu(w.styleSheet()))

    # RESET SELECTION
    def resetStyle(self, widget):
        for w in self._ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.deselectMenu(w.styleSheet()))

    def resize_grips(self):
        if self.app_config.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def resizeEvent(self, event):
        # Update Size Grips
        self.resize_grips()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        #if event.buttons() == Qt.LeftButton:
        #    print(f'Mouse click: LEFT CLICK {self.dragPos}')
        #if event.buttons() == Qt.RightButton:
        #    print('Mouse click: RIGHT CLICK')

    def mouseMoveEvent(self, event) -> None:
        # IF MAXIMIZED CHANGE TO NORMAL

        if self.returStatus():
            self.maximize_restore()
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            print(f"Mouse move: {event.pos()} - {self.pos()}")
            self.dragPos = event.globalPos()
            # event.accept()
            # self.update()

    def maximize_restore(self):
        status = self.GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self._ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self._ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self._ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self._ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self._ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self._ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self._ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self._ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return self.GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        self.GLOBAL_STATE = status
