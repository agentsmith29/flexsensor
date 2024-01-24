import traceback
from PySide6.QtWidgets import (
        QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit,
)
from PySide6.QtGui import QIcon

import FlexSensor.Prober as Prober

from FlexSensor.Prober.controller.ProberController import ProberController
from FlexSensor.Prober.controller.OpticalInterface import Probe


class StepThroughView(QMainWindow):
    def __init__(self, grouped_structures, prober: ProberController):
        super(StepThroughView, self).__init__()
        self.prober = prober
        self.grouped_structures = grouped_structures
        self.idx_struct = 0
        self.idx_group = 0
        self.init_UI()
        self.move_to_structure()
        self.msg_server = None
       

    def init_UI(self):
        # create a layout
        layout = QGridLayout()
        widget = QWidget()
        # add a label
        self.group_name = QLineEdit("This is a label")
        self.structure_name = QLineEdit("This is a label")
        # add a button
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.on_click_prev)

         # add a button
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.on_click_next)

        self.btn_search_for_light = QPushButton("Search for light")
        self.btn_search_for_light.clicked.connect(self.on_search_for_light)

        # Add the widgets to the layout
        layout.addWidget(self.group_name, 0, 0, 1, 2)
        layout.addWidget(self.structure_name, 1, 0, 1, 2)
        layout.addWidget(self.btn_prev, 2, 0)
        layout.addWidget(self.btn_next, 2, 1)
        

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #self.layout.setLayout(tree)

        self.setWindowTitle(f'Step Structure')   
        self.setWindowIcon(QIcon('icon.ico')) 

    def move_to_structure(self):
      
        self.group: str = list(self.grouped_structures)[self.idx_group]
        self.structures: dict = self.grouped_structures[self.group]
        self.structure: input_file_parser.Structure = list(self.structures.values())[self.idx_struct]
        try:
            #with Prober.velox_api.MessageServerInterface() as self.msg_server:
                #velox_api.MoveChuck(0, 0)
                #print(f"New structure group ({self.idx_groups}): {self.groups}. {len(structures)} structures in group.")


                # Move to die
                #print(f"Move chuck (first probe) to X({self.structure.x_in}), Y({self.structure.y_in}).")
                self.prober.move_chuck(self.structure.x_in, self.structure.y_in)

                try:
                    if self.structure.in_out_diff_x > 50:
                        #print(
                        #    f"Move second probe to X({self.structure.x_out}), Y({self.structure.y_out}) "
                        #    f"- Difference x({self.structure.in_out_diff_x}) y({self.structure.in_out_diff_y})"
                        #)
                        self.prober.opt_if.move_optical_probe(Probe.OUTPUT, self.structure.in_out_diff_x, self.structure.in_out_diff_y, pos_ref="H")
                        #self.msg_server.sendSciCommand("MoveOpticalProbe",rparams='1 %s %s H' %
                        #    (self.structure.in_out_diff_x, self.structure.in_out_diff_y)
                        #)
                    else:
                        raise Exception("Optical Probe Home not safe! x difference < 50 um: {self.structure.in_out_diff_x}")
                except Exception as e:
                    print("error", f"Can't move optical probe safely. {e}")
                    print((
                        type(e), f"Can't move optical probe safely. {e}. Omitting Structure!", traceback.format_exc()
                    ))
                    print("warning", f"[!] Omitting structure {self.structure.name}")
        except Exception as e:
            print("error", f"Can't move optical probe safely. {e}")
            print((
                   type(e), f"Can't move optical probe safely. {e}. Omitting Structure!", traceback.format_exc()
                ))  

        self.group_name.setText(f"Group: {self.group}")
        self.structure_name.setText(f"Structure: {self.structure.name}")

    def on_search_for_light(self):
        self.prober.opt_if.store_optical_probe_pos()
        #self.prober.opt_if.restore_optical_probe_motor_pos(probe=Probe.INPUT)
        #self.prober.opt_if.restore_optical_probe_motor_pos(probe=Probe.OUTPUT)

    
    def on_click_prev(self):
        self.idx_struct = self.idx_struct - 1
        if self.idx_struct < 0:
            self.idx_group =  self.idx_group - 1
            if self.idx_group < 0:
                self.idx_group = len(self.grouped_structures) - 1
            
            group: str = list(self.grouped_structures)[self.idx_group]
            self.idx_struct = len(self.grouped_structures[group]) - 1
        self.move_to_structure()

    def on_click_next(self):
        self.idx_struct = self.idx_struct + 1
        if self.idx_struct >= len(self.structures):
            self.idx_group =  self.idx_group + 1
            if self.idx_group >= len(self.grouped_structures):
                self.idx_group = 0
            self.idx_struct = 0
        self.move_to_structure()
        
        