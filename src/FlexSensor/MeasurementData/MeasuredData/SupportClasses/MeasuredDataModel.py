from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, Signal
import collections

from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget

from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData


class MeasuredDataTree(QTreeWidget):

    selected_data_changed = Signal(int)

    def __init__(self, measured_data_list: list[SingleMeasuredData]):
        super().__init__()
        self.setHeaderLabels(['Name', 'Xin', 'Yin', 'Xout', 'Yout', 'number'])
        self.grouped_data = {}
        self.measured_data_list = measured_data_list
        for it, data in enumerate(self.measured_data_list):
            if data.wafer_properties.wafer_number not in self.grouped_data:
                self.grouped_data[data.wafer_properties.wafer_number] = {}
            if data.wafer_properties.die_number not in self.grouped_data[data.wafer_properties.wafer_number]:
                self.grouped_data[data.wafer_properties.wafer_number][data.wafer_properties.die_number] = []
            self.grouped_data[data.wafer_properties.wafer_number][data.wafer_properties.die_number].append((data, it))
        self.populate_tree()




    def populate_tree(self):

        for wafer, die_dict in self.grouped_data.items():
            wafer_item = QTreeWidgetItem([f'Wafer {wafer}'])
            for die, data_list in die_dict.items():
                die_item = QTreeWidgetItem([f'Die {die}'])
                for data in data_list:
                    data, it = data
                    print(it)
                    data_item = QTreeWidgetItem([
                        data.wafer_properties.structure_name,
                        str(data.wafer_properties.structure_x_in),
                        str(data.wafer_properties.structure_y_in),
                        str(data.wafer_properties.structure_x_out),
                        str(data.wafer_properties.structure_y_out),
                        str(it)
                    ])
                    die_item.addChild(data_item)
                wafer_item.addChild(die_item)
            self.addTopLevelItem(wafer_item)

    # def selected_data(self):
    #     item = self.currentItem()
    #     if item.parent():
    #         # Return MeasuredData instance for selected die
    #         wafer_item = item.parent()
    #         wafer_num = int(wafer_item.text(0).split()[-1])
    #         die_num = int(item.text(0).split()[-1])
    #         for data in self.measured_data_list:
    #             if data.wafer_number == wafer_num and data.die_number == die_num:
    #                 return data
    #     else:
    #         # Return None for selected wafer
    #         return None

    def mouseDoubleClickEvent(self, event):

        item = self.currentItem()
        print(item)
        if item:
            self.selected_data_changed.emit(int(item))
