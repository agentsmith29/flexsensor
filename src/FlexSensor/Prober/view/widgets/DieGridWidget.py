import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel

from Prober.controller.MapFileParser import MapFileParser
from Prober.model.ProberModel import ProberModel


class FlatButton(QPushButton):
    def __init__(self, text, top_left="", top_right="", bottom_left="", bottom_right="", parent=None):
        super().__init__(parent, text)

        # Set flat appearance

        self.setFlat(True)

        self.color_default = QColor(192, 192, 192)#QColor(0, 58, 98) #
        self.color_die_selected = QColor(49, 61, 102)
        self.color_probe_active = QColor(62, 120, 52)
        self.color_disabled = QColor(0, 0, 0)
        self.border_color = self.color_default

        self.setStyleSheet(self.get_stylesheet(self.color_default))

        # Set quadratic aspect ratio
        self.setMaximumSize(50, 50)
        self.setMinimumSize(50, 50)
        self.setFixedSize(50, 50)

        self.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        # Create label widgets
        #self.top_left_label = QLabel(top_left, parent=self)
        self.top_right_label = QLabel(top_right, parent=self)
        self.bottom_left_label = QLabel(bottom_left, parent=self)
        self.bottom_right_label = QLabel(bottom_right, parent=self)

        # Set label positions
        #self.top_left_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.top_right_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.bottom_left_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.bottom_right_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        # Border colo


        # Border flag
        self.draw_border = False
        # Border width
        self.border_width = 3

    def get_stylesheet(self, qcolor):
        return f"background-color: rgb({qcolor.red()}, {qcolor.green()}, {qcolor.blue()});"
    def setTopLeftLabel(self, text):
        self.top_left_label.setText(text)

    def setTopRightLabel(self, text):
        self.top_right_label.setText(text)

    def setBottomLeftLabel(self, text):
        self.bottom_left_label.setText(text)

    def setBottomRightLabel(self, text):
        self.bottom_right_label.setText(text)

    def setEnabled(self, arg__1: bool) -> None:
        super().setEnabled(arg__1)
        if not arg__1:
            self.setStyleSheet(self.get_stylesheet(self.color_disabled))
            self.border_color = self.color_disabled # Black
            self.update()

    def set_die_selected(self, checked: bool) -> None:
        if not self.isEnabled():
            return

        if checked:
            self.setStyleSheet(self.get_stylesheet(self.color_die_selected))
            self.border_color = self.color_die_selected
        else:
            self.setStyleSheet(self.get_stylesheet(self.color_default))
            self.border_color = self.color_default
        self.update()

    def set_probe_active(self, active: bool) -> None:
        if not self.isEnabled():
            return

        if active:
            #self.setStyleSheet(self.get_stylesheet(self.color_default))
            self.border_color = self.color_probe_active
        else:
            #self.setStyleSheet(self.get_stylesheet(self.color_default))
            self.border_color = self.color_default
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        #if self.draw_border:
        painter = QPainter(self)
        pen = QPen(self.border_color, self.border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(
            self.border_width // 2,
            self.border_width // 2,
            self.width() - self.border_width,
            self.height() - self.border_width
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Calculate label sizes based on button size
        button_size = self.size()
        border_offset = self.border_width // 2
        label_width = (button_size.width() - self.border_width)
        label_height = (button_size.height()) // 2

        # Set label sizes and positions


        self.top_right_label.setGeometry(self.border_width, self.border_width,
                                         label_width-self.border_width, label_height)

        self.bottom_left_label.setGeometry(self.border_width, label_height - self.border_width,
                                           label_width//2, label_height)

        self.bottom_right_label.setGeometry(label_width//2,  label_height - self.border_width,
                                            label_width//2+1, label_height)



class DieGridWidget(QWidget):
    def __init__(self, model: ProberModel):
        super(DieGridWidget, self).__init__()
        self._model = model

        parsed_map = MapFileParser(str(self._model.wafer_map))
        self.setWindowTitle("Die Grid Widget")
        self._dies = {}

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)
        #self.grid_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

        self.setLayout(self.grid_layout)

        self._die = parsed_map.result['Die']

        self._prof_dies = parsed_map.result['ProfDies']
        self.create_die_grid()
        self.setFixedSize(9*60, 9*60)


        self._model.signals.die_changed.connect(self.update_die_grid)

        self.update_die_grid(self._model.die)

    def create_die_grid(self):
        table = pd.DataFrame([[int(die), *self._die[die].split(",")] for die in self._die],
                             columns=['die_number', 'col', 'row', 'status'])
        table['col'] = table['col'].astype(int)
        table['row'] = table['row'].astype(int)
        table['status'] = table['status'].astype(str)

        table['col_os'] = table.apply([lambda row: row['col'] - table['col'].min()], axis=1)
        table['row_os'] = table.apply([lambda row: row['row'] - table['row'].min()], axis=1)
        

        #print(table)
        # pd.DataFrame([die.split(",").strip for die in die_info], columns=['col', 'row', 'status'])
        for entry in self._prof_dies:
            col, row, value = self._prof_dies[entry].split(",")
            df = table.loc[(table['col'] == int(col)) & (table['row'] == int(row))]
            if df.empty:
                continue
            else:
                table.loc[(table['col'] == int(col)) & (table['row'] == int(row)), 'prof_die_number'] = entry
        

        for index, die in table.iterrows():
            button = FlatButton("1", "2", f"{die['col']}, {die['row']}",  str(die['die_number']), str(die['status']))#,
            if die['status'] == "X":
                button.setEnabled(False)
            elif die['status'] == "V":
                    button.set_die_selected(False)
            elif die['status'] == "P":
                button.set_die_selected(True)
                #button.setText(f"{die['col']}, {die['row']} - {die['die_number']}")
            self._dies[f"{die['row']}, {die['col']}"] = button

            button.clicked.connect(self.on_button_clicked)

            self.grid_layout.addWidget(button, die['col_os'], die['row_os'])

        #print(table)

    def on_button_clicked(self):
        button: FlatButton = self.sender()
        button.set_probe_active(True)

    def update_die_grid(self, die):
        for die in self._dies:
            self._dies[die].set_probe_active(False)

        die_x = self._model.die_row
        die_y = self._model.die_col
        print(f"Die {die}: {die_x}, {die_y} was probed")
        #print(self._dies)
        self._dies[f"{die_x}, {die_y}"].set_probe_active(True)
        

if __name__ == "__main__":
    app = QApplication([])

    parsed_map = MapFileParser("../Wafermapary1_48dies.map")

    widget = DieGridWidget(parsed_map)
    widget.show()

    app.exec_()