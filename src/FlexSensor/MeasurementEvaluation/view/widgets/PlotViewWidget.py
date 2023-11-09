import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg  import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox

matplotlib.use('QT5Agg')

class PlotViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Matplotlib figure and axes
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.plot_selection = ""

        # Add the canvas to this PySide6 widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Set up the initial graph with no data
        self.ax.set_xlabel('Wavelength')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.grid(True)
