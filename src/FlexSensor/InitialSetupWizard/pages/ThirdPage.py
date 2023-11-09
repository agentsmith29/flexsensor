from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QLineEdit

import Prober as Prober
from InitialSetupWizard.pages.WizardPage import WizardPage


class ThirdWizardPage(WizardPage):
    def __init__(self, prober: Prober.Controller, parent=None):
        super().__init__(prober, parent)

        self.setTitle("Selecting the reference structure.")
        layout = QGridLayout()
        # ==============================================================================================================
        task_moved_to_ref_structure, _ = self.add_task(
            "1. Place the Scope over the Input Probe.",
            "Try to match the center point using the scope's cross. It is useful to set the scope home position to the"
            "current position.", "task_moved_scope*")

        layout.addWidget(task_moved_to_ref_structure, 0, 0, 1, 4)
        graphics1 = self.add_graphics(f'{self.imgf}/Step2_1.png')
        layout.addWidget(graphics1, 1, 0, 1, 4)

        # ==============================================================================================================
        task_move_to_home, _ = self.add_task(
            "2.  Move back to the zero position",
            "Move back to the 'zero' point. This point is your arbitrarily chosen reference point and must be the same "
            "in your layout file and the prober. Usually a mark or the die's corner is used, however not mandatory.\n"
            "Input the X and y distance from the calibration structure to the 'zero' point. Make sure to have the "
            "signs correct.",
            "task_set_chuck_home_position*")
        layout.addWidget(task_move_to_home, 2, 0, 1, 4)
        # Input the X and y distance from the calibration structure to the Home Position
        graphics1 = self.add_graphics(f'{self.imgf}/Step2_2.png', max_width=400)
        layout.addWidget(graphics1, 3, 0, 1, 4)
        self.lbl_movement_x = QLabel("X Movement: ")
        self.input_movement_x = QLineEdit("-950")

        layout.addWidget(self.lbl_movement_x, 4, 0)
        layout.addWidget(self.input_movement_x, 4, 1)

        self.input_movement_y = QLabel("Y Movement: ")
        self.lbl_movement_y = QLineEdit("2120")
        layout.addWidget(self.input_movement_y, 4, 2)
        layout.addWidget(self.lbl_movement_y, 4, 3)

        self.btn_move_to_home = QPushButton('Move chuck')
        layout.addWidget(self.btn_move_to_home, 5, 0, 1, 4)
        self.btn_move_to_home.clicked.connect(
            lambda: self.move_chuck_x_y(int(self.input_movement_x.text()), int(self.lbl_movement_y.text())))

        # ==============================================================================================================
        task_set_chuck_home_position, _ = self.add_task(
            "3.  Set Chuck Home position",
            "Use the 'Set to Current Position' to the left to reset the prober's coordinates to (0,0,Z)",
            "task_set_chuck_home_position*")
        layout.addWidget(task_set_chuck_home_position, 6, 0, 1, 4)
        # layout.addWidget(self.add_graphics(path=f'{self.imgf}/1_placed_at_origin_cut.JPG'), 7, 0, 1, 4)
        self.btn_move_to_home = QPushButton('Set chuck Home')
        layout.addWidget(self.btn_move_to_home, 7, 0, 1, 4)
        self.btn_move_to_home.clicked.connect(lambda: self.prober.set_chuck_home())

        self.setLayout(layout)

    # def get_distance(self) -> float:
    #     value = self.input_distance.text()
    #     try:
    #         distance = int(value)
    #     except Exception as e:
    #         self.logger.error(f"Can't convert {value} to int!")
    #         raise e
    #     return distance
    #
    # def move_chuck(self):
    #     distance = self.get_distance()
    #     distance_half = int(distance / 2)
    #     self.move_chuck_x_y(x=-distance_half, y=0)
