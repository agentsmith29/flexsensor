import sys

from PySide6.QtWidgets import QWizard, QApplication

import Prober as Prober
from InitialSetupWizard.pages.FifthPage import FifthWizardPage
from InitialSetupWizard.pages.ForthPage import ForthWizardPage
from InitialSetupWizard.pages.ThirdPage import ThirdWizardPage
from InitialSetupWizard.pages.SecondPage import SecondWizardPage
from InitialSetupWizard.pages.FirstPage import FirstWizardPage


class InitialSetupWizard(QWizard):

    def __init__(self, prober: Prober.Controller, parent=None):
        super().__init__(parent)
        self.prober = prober
        self.addPage(FirstWizardPage(self.prober, self))
        self.addPage(SecondWizardPage(self.prober, self))
        p3 = ThirdWizardPage(self.prober, self)
        self.addPage(p3)
        p4 = ForthWizardPage(self.prober, p3, parent=self)
        self.addPage(p4)
        self.addPage(FifthWizardPage(self.prober, p4, self))

        self.setWindowTitle("Wizard Example")


if __name__ == "__main__":

    app = QApplication()
    prober = Prober.Controller()
    wizard = InitialSetupWizard(prober)

    wizard.show()

    sys.exit(app.exec())

