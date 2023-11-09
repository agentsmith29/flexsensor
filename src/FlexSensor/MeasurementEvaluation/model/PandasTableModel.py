from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QMenu


class PandasTableModel(QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):

        return self.df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.df.iloc[row, col])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.df.columns[section])
            elif orientation == Qt.Vertical:
                return str(self.df.index[section])
        return None
