from PySide6.QtWidgets import QWizard, QGridLayout, QLabel, QPushButton

import Prober as Prober
from InitialSetupWizard.pages.ForthPage import ForthWizardPage
from InitialSetupWizard.pages.WizardPage import WizardPage


class FifthWizardPage(WizardPage):
    def __init__(self, prober: Prober.Controller, page_input_distance: ForthWizardPage, parent: QWizard = None):
        super().__init__(prober, parent)
        self.setMaximumHeight(450)
        self.setMinimumHeight(450)

        self.setTitle("Train Output Home Position")
        layout = QGridLayout()
        self.distance = 0
        # p_3: ThirdPage = parent.page(2)
        page_input_distance.input_distance.textChanged.connect(self._on_distance_changed)
        self.label_intro = QLabel(
            f"To train the output home Position the Prober will move both probes in the direction given in the previous"
            f"step. \n"
            f"First it will move the input probe 500um to the left, then the output probe the given distance "
            f"d={self.distance}um so it is placed at the input position. \n"
            f"Afterwards the Home position is set to the current "
            f"position and both probes are moved back to it's initial position.")
        self.label_intro.setWordWrap(True)
        layout.addWidget(self.label_intro, 0, 0, 1, 2)

        self.btn_train = QPushButton('Set Home Position')
        self.btn_train.clicked.connect(lambda: self.train_warn(self.distance))
        layout.addWidget(self.btn_train, 1, 0, 1, 2)

        self.setLayout(layout)

    def _on_distance_changed(self, distance):
        self.distance = int(distance)
        self.label_intro.setText(
            f"To train the output home Position the Prober will move both probes in the direction given in the previous"
            f"step. \n"
            f"First it will move the input probe 500um to the left, then the output probe the given distance "
            f"d={self.distance}um so it is placed at the input position. \n"
            f"Afterwards the Home position is set to the current "
            f"position and both probes are moved back to it's initial position.")

    # NO pressed

    def train_warn(self, distance, safe_move_distance=500):
        # Bevor continuning display a warning as a dialog box to the user
        if self.display_mbox_warning(
                text=f"The output optical probes are about to move {distance} towards the input probe. The"
                     f" input probe will be moved away {safe_move_distance}."
                     f"Make sure that no obstacles are in the way and the distance is safe to move.",
                title="Optical probe are about to move"
        ):
            self.train(distance, safe_move_distance)
        else:
            self.display_mbox_error(text="The movement has been aborted by the user.", title="Movement Aborted.")
            return

    def train(self, distance, safe_move_distance):
        # First read out both positions
        x_in, y_in, z_in, _, _, _ = self.prober.opt_if.set_optical_probe_home(probe=Prober.Probe.INPUT)
        x_out, y_out, z_out, _, _, _ = self.prober.opt_if.set_optical_probe_home(probe=Prober.Probe.OUTPUT)
        pos = Prober.ProbePosition(input=(x_in, y_in, z_in), output=(x_out, y_out, z_out))
        print(pos)
        # Now move the input probe away from the position

        # INPUT -safe_move_distance #===================================================================================
        self.logger.info(f"Moving input probe {-safe_move_distance}um.")
        self.prober.opt_if.move_optical_probe(Prober.Probe.INPUT, -safe_move_distance, '0', 'R')
        self.logger.info(f"Moved input probe {-safe_move_distance}um.")
        # ==============================================================================================================

        # OUTPUT -distance =============================================================================================
        self.logger.info(f"Moving output probe {-distance}um.")
        if self.display_mbox_warning(
                text=f"The  optical output probe is about to move {-distance}um towards the input probe. "
                     f"Make sure that the output probe has been moved!",
                title="Optical output probe are about to move",
        ):
            self.prober.opt_if.move_optical_probe(Prober.Probe.OUTPUT, -distance, '0', 'R')
            self.logger.info(f"Moved output probe {-distance}um.")
        else:
            self.display_mbox_error(text="The movement has been aborted by the user.", title="Movement Aborted.")
            return
        # ==============================================================================================================

        # ==============================================================================================================
        self.prober.opt_if.set_optical_probe_home(Prober.Probe.OUTPUT)
        self.logger.info(f"Set optical output home to current position")
        # ==============================================================================================================

        # OUTPUT distance ==============================================================================================
        self.logger.info(f"Moving output probe {distance}um back to initial position ")
        self.prober.opt_if.move_optical_probe(Prober.Probe.OUTPUT, distance, '0', 'R')
        # ==============================================================================================================

        # INPUT safe_move_distance =====================================================================================
        self.logger.info(f"Moving input probe {safe_move_distance}um back to initial position.")
        if self.display_mbox_warning(
                text=f"The optical input probe is about to move {safe_move_distance}um towards the output probe. "
                     f"Make sure that the output probe position has been reset!",
                title="Optical output probe are about to move"
        ):
            self.prober.opt_if.move_optical_probe(Prober.Probe.INPUT, safe_move_distance, '0', 'R')
            self.logger.info(f"Moved input probe {safe_move_distance}.")
        else:
            self.display_mbox_error(text="The movement has been aborted by the user.", title="Movement Aborted.")
            return
        # ==============================================================================================================
        self.display_mbox_ok(text="The home position has been set successfully!",
                             title="Home position set")
