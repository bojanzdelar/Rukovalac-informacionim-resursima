from PySide2 import QtCore

class StudentModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.students = []

    def get_element(self, index):
        return self.students[index.row()]

    def rowCount(self, index):
        return len(self.students)

    def columnCount(self, index):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        student = self.get_element(index)
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return student.ustanova
        elif index.column() == 1 and role == QtCore.Qt.DisplayRole:
            return student.broj_indeksa
        elif index.column() == 2 and role == QtCore.Qt.DisplayRole:
            return student.prezime
        elif index.column() == 3 and role == QtCore.Qt.DisplayRole:
            return student.ime
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if section == 0 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Ustanova"
        elif section == 1 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Broj indeksa"
        elif section == 2 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Prezime"
        elif section == 3 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Ime"

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        student = self.get_element(index)
        if value == "":
            return False
        if index.column() == 0 and role == QtCore.Qt.EditRole:
            student.ustanova = value
            return True
        elif index.column() == 1 and role == QtCore.Qt.EditRole:
            student.broj_indeksa = value
            return True
        elif index.column() == 2 and role == QtCore.Qt.EditRole:
            student.prezime = value
            return True
        elif index.column() == 3 and role == QtCore.Qt.EditRole:
            student.ime = value
        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable