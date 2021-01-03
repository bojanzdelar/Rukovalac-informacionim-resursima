from PySide2 import QtCore
from .serial_file import SerialFile
from .sequential_file import SequentialFile
from .database import Database

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent_dir, file_name, parent=None):
        super().__init__(parent)
        if parent_dir == "serial":
            self.information_resource = SerialFile(file_name)
        elif parent_dir == "sequential":
            self.information_resource = SequentialFile(file_name)
        elif parent_dir == "database":
            self.information_resource = Database(file_name)
            
    def get_element(self, index):
        return self.information_resource.read_element(index.row())
  
    def rowCount(self, index=None):
        return len(self.information_resource.data)

    def columnCount(self, index=None):
        return len(self.information_resource.get_attribute())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if index.column() == i and role == QtCore.Qt.DisplayRole:
                return str(self.get_element(index)[i])

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(self.columnCount()):
            if section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.information_resource.get_attribute(i)["name"]