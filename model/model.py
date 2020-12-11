from PySide2 import QtCore
from .informacioni_resurs import InformacioniResurs

class Model(QtCore.QAbstractTableModel):
    def __init__(self, file_name, parent=None):
        super().__init__(parent)
        self.informacioni_resurs = InformacioniResurs(file_name)

    def get_element(self, index):
        return self.informacioni_resurs.data[index.row()]
  
    def rowCount(self, index=None):
        return len(self.informacioni_resurs.data)

    def columnCount(self, index=None):
        return len(self.informacioni_resurs.get_attributes())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if index.column() == i and role == QtCore.Qt.DisplayRole:
                return self.get_element(index)[i]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.informacioni_resurs.get_attribute(i)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if value == "":
            return False
        for i in range(self.columnCount()):
            if index.column() == i and role == QtCore.Qt.EditRole:
                self.get_element(index)[i] = value
                return True
        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable