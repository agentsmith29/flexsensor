from PySide6.QtCore import Signal, Qt, QObject
from PySide6.QtGui import QStandardItem, QStandardItemModel, QAction
from PySide6.QtWidgets import (QTreeView, QVBoxLayout, QWidget, QTableView, QTableWidgetItem, QTableWidget, QMainWindow,
                               QAbstractItemView, QMenu)

import MeasurementData
from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData


class MultipleMeasurementItem(QStandardItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def type(self, *args, **kwargs):
        return 'Multi'


class SingleMeasurementItem(QStandardItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def type(self):
        return 'Single'


class MeasurementSelectionWidgetSignals(QObject):
    open_find_peaks_window = Signal(list)
    on_consolidate_measurement_clicked = Signal(list)
    on_recalculation_clicked = Signal(list)
    on_show_item_click = Signal(SingleMeasuredData)


class MeasurementSelectionWidget(QMainWindow):
    consolidate_data = Signal(SingleMeasuredData)

    def __init__(self, data):
        super().__init__()
        self.data: dict[str, dict[int, dict[str, list[SingleMeasuredData]]]] = data

        self.signals = MeasurementSelectionWidgetSignals()

        self.tree_view = QTreeView(self)
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)

        self.setup_model()
        self.tree_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)
        self.setCentralWidget(self.tree_view)

    def setup_model(self):
        for k1, v1 in self.data.items():
            parent_item = QStandardItem(k1)
            self.model.appendRow(parent_item)
            for k2, v2 in v1.items():
                child_item = QStandardItem(str(k2))
                parent_item.appendRow(child_item)
                for k3, v3 in v2.items():
                    sub_child_item = MultipleMeasurementItem(k3)
                    child_item.appendRow(sub_child_item)
                    sub_child_item.setData(list(v2.values())[0])
                    for measured_data in v3:
                        data_item = SingleMeasurementItem(str(measured_data))
                        sub_child_item.appendRow(data_item)
                        data_item.setData(measured_data)

    def multi_selection_menu(self, pos):
        menu = QMenu(self)

        action = QAction("Recalculate", self)
        action.triggered.connect(self._on_recalculation_clicked)
        menu.addAction(action)

        action = QAction("Consolidate Data", self)
        action.triggered.connect(self._on_consolidate_data_clicked)
        menu.addAction(action)

        action = QAction("Adapt 'FindPeaks' parameters", self)
        action.triggered.connect(self._on_adapt_parameters_clicked)
        menu.addAction(action)


        menu.exec_(self.tree_view.viewport().mapToGlobal(pos))

    def single_selection_menu(self, pos):
        menu = QMenu(self)
        action = QAction("Add to view", self)
        action.triggered.connect(self._on_show_item_clicked)
        menu.addAction(action)
        menu.exec_(self.tree_view.viewport().mapToGlobal(pos))

    def show_context_menu(self, pos):
        selection = self.tree_view.selectionModel()
        index = selection.currentIndex()
        if index.isValid():
            item = self.model.itemFromIndex(index)
            if item is not None:
                if isinstance(item, SingleMeasurementItem):
                    self.single_selection_menu(pos)
                elif isinstance(item, MultipleMeasurementItem):
                    self.multi_selection_menu(pos)

    def _on_show_item_clicked(self):
        selection = self.tree_view.selectionModel()
        data = self.on_clicked_acquire_item_data(selection)
        self.signals.on_show_item_click.emit(data)

    def _on_recalculation_clicked(self):
        selection = self.tree_view.selectionModel()
        data = self.on_clicked_acquire_item_data(selection)
        self.signals.on_recalculation_clicked.emit(data)

    def _on_adapt_parameters_clicked(self):
        selection = self.tree_view.selectionModel()
        data = self.on_clicked_acquire_item_data(selection)
        self.signals.open_find_peaks_window.emit(data)

    def _on_consolidate_data_clicked(self):
        selection = self.tree_view.selectionModel()
        data = self.on_clicked_acquire_item_data(selection)
        self.signals.on_consolidate_measurement_clicked.emit(data)

    def on_clicked_acquire_item_data(self, selection):
        index = selection.currentIndex()
        if index.isValid():
            item = self.model.itemFromIndex(index)
            if item.parent() is not None:
                return item.data()
        return None