from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

import Prober as Prober
from InitialSetupWizard.pages.WizardPage import WizardPage


class SecondWizardPage(WizardPage):

    def __init__(self, prober: Prober.Controller, parent=None):
        super().__init__(prober, parent)
        self.setTitle("Initial Setup")
        self.setSubTitle("In this step, the home position will be set.")

        layout = QVBoxLayout()
        labeli = QLabel("The structure file relies on 'relative' positions to a 'zero' point. Usually such a suitable"
                        "structure can be chosen as the 'die' origin. From this 'zero' position, "
                        "every coordinates (x, y) is used to measure the distance to"
                        "the to/be measured structures.")
        labeli.setWordWrap(True)
        layout.addWidget(labeli)

        label1 = QLabel("Use the same 'mark' in the Klayout file and on the wafer. Usually the die's edge is a good"
                        "point.\n")
        layout.addWidget(label1)

        # ==============================================================================================================
        task_move_chuck, _ = self.add_task(
            "1.  Manually move chuck to the calibration structure",
            "Manually move the Chuck to the calibration structure using the the Velox Chuck Control. "
            "Then move the Probes using the FFI Photonic Interface to place it exaclty above the grating couplers.",
            "task_move_chuck*")
        layout.addWidget(task_move_chuck)
        layout.addWidget(self.add_graphics(path=f'{self.imgf}/Step2_1.png'))

        # ==============================================================================================================
        task_area_scan, self.cb_area_scan = self.add_task(
            "2.  Perform an 'Area Scan'",
            "If the Probes are moved, perform an 'Area Scan' to find the best position of the probes."
            "The program may freez during the area scan.",
            "task_area_scan*")
        self.cb_area_scan.setCheckable(True)
        layout.addWidget(task_area_scan)
        self.btn_area_scan = QPushButton('Perform Area Scan (Input/Output)')
        self.txt_coupled_power = QLabel('In: N/A, Out:N/A - Not performed.')
        layout.addWidget(self.btn_area_scan)
        layout.addWidget(self.txt_coupled_power)
        self.btn_area_scan.clicked.connect(lambda: self.area_scan(self.txt_coupled_power, self.cb_area_scan))

        self.setLayout(layout)

