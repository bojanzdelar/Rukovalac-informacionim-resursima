from PySide2 import QtCore
from model.visokoskolska_ustanova import VisokoskolskaUstanova
from model.student import Student
import json

class Model(QtCore.QAbstractTableModel):
    def __init__(self, file_name, parent=None):
        super().__init__(parent)
        self.file_name = file_name
        self.info = self.read_meta()
        self.list = []
        self.load()

    def attributes(self):
        return len(self.get_attributes())

    def get_element(self, index):
        return self.list[index.row()]

    def get_attributes(self):
        return self.info["attributes"]

    def get_subtables(self):
        return self.info["subtables"]

    def rowCount(self, index):
        return len(self.list)

    def columnCount(self, index):
        return len(self.get_attributes())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        element = self.get_element(index)
        for i in range(self.attributes()):
            if index.column() == i and role == QtCore.Qt.DisplayRole:
                return element.data[self.get_attributes()[i]]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(self.attributes()):
            if section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.get_attributes()[i]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        element = self.get_element(index)
        if value == "":
            return False
        for i in range(self.attributes()):
            if index.column() == i and role == QtCore.Qt.EditRole:
                element.data[self.get_attributes()[i]] = value
                return True
        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def read_meta(self):
        with open("meta.json") as file:
            data = json.load(file)
        return data[self.file_name]

    def load(self):
        if self.file_name == "visokoskolske_ustanove.csv":
            self.list = VisokoskolskaUstanova.load()
        elif self.file_name == "studenti.csv":
            self.list = Student.load()