from PySide2 import QtCore
from .information_resource import InformationResource

class Model(QtCore.QAbstractTableModel):
    def __init__(self, file_name, parent=None):
        super().__init__(parent)
        self.information_resource = InformationResource(file_name)

    def get_element(self, index):
        return self.information_resource.read_element(index.row())
  
    def rowCount(self, index=None):
        return len(self.information_resource.data)

    def columnCount(self, index=None):
        return len(self.information_resource.get_attribute())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if index.column() == i and role == QtCore.Qt.DisplayRole:
                return self.get_element(index)[i]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.information_resource.get_attribute(i)["name"]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if value == "":
            return False
        for i in range(self.columnCount()):
            if index.column() == i and role == QtCore.Qt.EditRole:
                self.get_element(index)[i] = value
                return True
        return False