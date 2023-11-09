from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox

import Prober as Prober
from InitialSetupWizard.pages.ThirdPage import ThirdWizardPage
from InitialSetupWizard.pages.WizardPage import WizardPage


class ForthWizardPage(WizardPage):
    def __init__(self, prober: Prober.Controller, third_page: ThirdWizardPage, parent=None):
        super().__init__(prober, parent)
        self.third_page = third_page
        self.setTitle("Positioning of the Probes")
        layout = QGridLayout()

        task_set_chuck_home_position, _ = self.add_task(
            "1.  Move to the calibration structure",
            "Click on the next button 'Move to calibration structure' to move the chuck back to the calibration structure.\n"
            "Warning: The probes will be moved 250um away from the selected position to ease the next step.",
            "task_move_back_to_cal_structure*")
        layout.addWidget(task_set_chuck_home_position, 1, 0, 1, 4)

        # ==============================================================================================================
        # layout.addWidget(self.add_graphics(path=f'{self.imgf}/1_placed_at_origin_cut.JPG'), 10, 0, 1, 4)
        self.btn_move_back_to_cal_structure = QPushButton('Move to calibration structure')
        layout.addWidget(self.btn_move_back_to_cal_structure, 2, 0, 1, 4)
        self.btn_move_back_to_cal_structure.clicked.connect(lambda: self.move_back_to_cal_structure(probe_movement=250))

        task_measure_distance, _ = self.add_task(
            "2.  Measure the distance between the input and the output.",
            "For calibrating the position of the input probe to the output probe, "
            "the difference of the input and the output must be determined. If the "
            "distance is not known, Velox's Measurement Tool can be used. \n"
            "Note: If using layout values make sure to include a distance which "
            "corresponds to the position of input and the output probes",
            "measure_distance*")
        layout.addWidget(task_measure_distance, 3, 0, 1, 4)

        graphics1 = self.add_graphics(f'{self.imgf}/Step4_2.png')
        layout.addWidget(graphics1, 4, 0, 1, 4)

        self.task_enter_distance, self.cb_distance_enterd = self.add_task(
            "3.  Enter the (measured) distance between input and output.",
            "Enter the measured distance below and press 'Apply' to move the chuck half the given distance",
            "task_measure_distance*")
        layout.addWidget(self.task_enter_distance, 5, 0, 1, 4)
        self.cb_distance_enterd.setCheckable(False)

        lbl_distance = QLabel("Distance (d)")
        self.input_distance = QLineEdit()

        # self.btn_apply = QPushButton('Move chuck')
        layout.addWidget(lbl_distance, 6, 0, 1, 1)
        layout.addWidget(self.input_distance, 6, 1, 1, 1)
        self.btn_measurement_done = QPushButton("Apply")
        layout.addWidget(self.btn_measurement_done, 6, 2, 1, 2)
        self.btn_measurement_done.clicked.connect(lambda: self.move_probes_back(probe_movement=250))
        self.registerField('distance*', self.input_distance)

        self.setLayout(layout)



    def move_back_to_cal_structure(self, probe_movement=250):
        self.move_chuck_x_y(-int(self.third_page.input_movement_x.text()), -int(self.third_page.lbl_movement_y.text()) )
        self.move_input_probes_x_y(-probe_movement, 0)
        self.move_output_probes_x_y(probe_movement, 0)

    def move_probes_back(self, probe_movement=250):
        self.move_input_probes_x_y(probe_movement, 0)
        self.move_output_probes_x_y(-probe_movement, 0)
        self.cb_distance_enterd: QCheckBox
        self.cb_distance_enterd.setCheckable(True)
        self.cb_distance_enterd.setChecked(True)
        self.completeChanged.emit()