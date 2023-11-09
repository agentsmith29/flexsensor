import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget
from pyqtgraph.dockarea import DockArea, Dock

from MainWindow.view import MainView


class ScopeWidget(QWidget):

    def __init__(self, parent_view: MainView):
        super().__init__()
        self.parent_view = parent_view
        layout = QVBoxLayout()
        area = DockArea()

        d1 = Dock("Analog Discovery 2")
        d2 = Dock("Filtered")
        area.addDock(d1, 'bottom')
        area.addDock(d2, 'bottom', d1)

        self.scope_original = pg.PlotWidget(title="AD2 Acquisition")
        # self.scope_original.plot(np.random.normal(size=100)*1e12)
        self.scope_original.plotItem.showGrid(x=True, y=True, alpha=1)
        d1.addWidget(self.scope_original)

        self.scope_filtered = pg.PlotWidget(title="Filtered Data")
        # self.scope_filtered.plot(np.random.normal(size=100))
        self.scope_filtered.plotItem.showGrid(x=True, y=True, alpha=1)
        d2.addWidget(self.scope_filtered)
        layout.addWidget(area)
        self.setMinimumWidth(800)
        self.setLayout(layout)
