from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSplashScreen

from FlexSensor.pathes import image_root


class SplashScreen:

    @staticmethod
    def _display_splash_screen():
        pixmap = QPixmap(f"{image_root}/FlexSensorSplashScreen.png")
        scale = 0.5
        pixmap = pixmap.scaled(QSize(int(1024 * scale), int(683 * scale)))
        splash = QSplashScreen(pixmap)
        # splash.setFixedHeight(300)
        splash.show()
        return splash