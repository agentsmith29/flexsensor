from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizard, QVBoxLayout, QLabel

import Prober as Prober
from InitialSetupWizard.pages.WizardPage import WizardPage


class FirstWizardPage(WizardPage):
    def __init__(self, prober: Prober.Controller, parent=None):
        super().__init__(prober, parent)

        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, QPixmap())

        layout = QVBoxLayout()

        self.setTitle("Train Output Home Position")

        label = QLabel("This wizard will guide you trough the calibration step. \n"
                       "During the process the Prober (Chuck, etc.) and the Optical Interface (Hexapods, etc.) will "
                       "move! The wizard won't start the movement automatically and each step "
                       "must be verified by the user and started manually.\n"
                       "\n"
                       "To prevent damage, the setup process are designed to check each steps. Thus,"
                       "checking the individual steps is required to continue the calibration.\n\n "
                       "Click 'Next' to start the wizard.")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)

        # Add an image to the QWizardPage
        layout.addWidget(label)

        self.setLayout(layout)
