import logging
import pathlib

import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizardPage, QLabel, QWidget, QCheckBox, QVBoxLayout, QMessageBox, QSizePolicy

import Prober as Prober
from pathes import image_root


class WizardPage(QWizardPage):
    def __init__(self, prober: Prober.Controller, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.prober = prober
        self.logger = logging.getLogger('Wizard')

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.parent.setMinimumWidth(780)
        self.parent.setMaximumHeight(900)
        self.parent.setMinimumHeight(900)

        self.imgf = f"{image_root}/wizard_img"

        # Stores all included graphics for later accessing via the resize Event
        self.graphics = []

    # ==================================================================================================================
    # For adding UI Elements
    # ==================================================================================================================
    def add_graphics(self, path, max_width=None):
        print(f"Added {path}")
        graphics = QLabel(self)
        pixmap = QPixmap(str(pathlib.PurePosixPath(path)))
        self._resize_graphics_on_resize_event(graphics, pixmap, max_width=max_width)
        self.graphics.append({"graphics": graphics, "pixmap": pixmap})
        return graphics

    def add_task(self, title, description, task_desc) -> (QWidget, QCheckBox):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        task = QCheckBox(title)
        task.setStyleSheet(
            "QCheckBox:unchecked{ color: red; }QCheckBox:checked{ color: black; }")
        label = QLabel(description)
        label.setWordWrap(True)
        layout.addWidget(task)
        layout.addWidget(label)
        self.registerField(task_desc, task)
        return widget, task

    # ==================================================================================================================
    # Message Boxes
    # ==================================================================================================================
    def display_mbox_warning(self, text, title):
        self.logger.warning(text)
        warning_dialog = QMessageBox()
        warning_dialog.setText(text)
        warning_dialog.setIcon(QMessageBox.Warning)
        warning_dialog.setWindowTitle(title)
        warning_dialog.show()
        warning_dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
        btn_ok = warning_dialog.button(QMessageBox.StandardButton.Ok)
        btn_abort = warning_dialog.button(QMessageBox.StandardButton.Abort)
        warning_dialog.exec()
        if warning_dialog.clickedButton() == btn_ok:
            return True
        elif warning_dialog.clickedButton() == btn_abort:
            return False

    def display_mbox_error(self, text, title):
        self.logger.error(text)
        warning_dialog = QMessageBox()
        warning_dialog.setText(text)
        warning_dialog.setIcon(QMessageBox.Critical)
        warning_dialog.setWindowTitle(title)
        warning_dialog.show()
        warning_dialog.exec()

    def display_mbox_ok(self, text, title):
        self.logger.error(text)
        warning_dialog = QMessageBox()
        warning_dialog.setText(text)
        warning_dialog.setIcon(QMessageBox.Information)
        warning_dialog.setWindowTitle(title)
        warning_dialog.show()
        warning_dialog.exec()

    # ==================================================================================================================
    # Prober Controls
    # ==================================================================================================================
    def move_chuck_x_y(self, x, y):
        if self.display_mbox_warning(f"The chuck is about to move relatively {x} in x-direction und {y} y-direction. "
                                     f"Continue?",
                                     "Move chuck"):
            self.prober.move_chuck(x_value=x, y_value=y, pos_ref="R")
            # Enable the next button when the user has entered a non-empty
            # string.
            # self.cb_distance_enterd.setCheckable(True)
            # self.cb_distance_enterd.setChecked(True)
            self.completeChanged.emit()
        else:
            self.display_mbox_error(text="The movement has been aborted by the user.", title="Movement Aborted.")
            return

    def area_scan(self, txt_coupled_power: QLabel, checkbox: QCheckBox, threshold: float = -70):
        x_1, x_2, y_1, y_2, input_power, output_power = self.prober.opt_if.area_scan(True, True)
        if input_power > threshold and output_power > threshold:
            checkbox.setCheckable(True)
            checkbox.setChecked(True)
            # self.distance_task.setCheckable(False)
            txt_coupled_power.setText(f'In: {input_power}, Out: {output_power} - Passed/Threshold < -70dB.')
            self.completeChanged.emit()
        else:
            txt_coupled_power.setText(f'In: {input_power}, Out: {output_power} - Not passed/Threshold < -70dB.')

    def move_input_probes_x_y(self, x: float, y: float):
        self.prober.opt_if.move_optical_probe(0, x, y, pos_ref='R')

    def move_output_probes_x_y(self, x: float, y: float):
        self.prober.opt_if.move_optical_probe(1, x, y, pos_ref='R')

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _resize_graphics_on_resize_event(self, graphics, pixmap, max_width=None):

        aspect_ratio = pixmap.height() / pixmap.width()
        if max_width is None:
            max_width = int(self.parent.width()*0.95)
        max_height = np.floor(aspect_ratio * max_width)
        # print(f"{aspect_ratio}: {max_width}x{max_height} - {max_height / max_width}")

        graphics.setPixmap(pixmap.scaled(QSize(max_width, max_height),
                                         Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.SmoothTransformation))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        # print(self.graphics)
        for ele in self.graphics:
            self._resize_graphics_on_resize_event(ele['graphics'], ele['pixmap'])
