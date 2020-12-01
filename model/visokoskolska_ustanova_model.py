from PySide2 import QtCore

class VisokoskolskaUstanovaModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ustanove = []

    def get_element(self, index):
        return self.ustanove[index.row()]

    def rowCount(self, index):
        return len(self.ustanove)

    def columnCount(self, index):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        ustanova = self.get_element(index)
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return ustanova.oznaka
        elif index.column() == 1 and role == QtCore.Qt.DisplayRole:
            return ustanova.naziv
        elif index.column() == 2 and role == QtCore.Qt.DisplayRole:
            return ustanova.adresa
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if section == 0 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Oznaka"
        elif section == 1 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Naziv"
        elif section == 2 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Adresa"

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        ustanova = self.get_element(index)
        if value == "":
            return False
        if index.column() == 0 and role == QtCore.Qt.EditRole:
            ustanova.oznaka = value
            return True
        elif index.column() == 1 and role == QtCore.Qt.EditRole:
            ustanova.naziv = value
            return True
        elif index.column() == 2 and role == QtCore.Qt.EditRole:
            ustanova.adresa = value
            return True
        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable