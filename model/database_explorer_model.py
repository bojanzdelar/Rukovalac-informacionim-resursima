from PySide6 import QtCore, QtGui
from model.database import Database
from meta.meta import get_display

class DatabaseExplorerModel(QtCore.QStringListModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        tables = Database.get_tables()
        tables = [table_name for tpl in tables for table_name in tpl]
        self.setStringList(tables)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if section == 0 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Relaciona baza podataka"
        return super().headerData(section, orientation, role)
    
    def data(self, index, role=QtCore.Qt.DecorationRole):
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return get_display(self.stringList()[index.row()], "database")
        elif index.column() == 0 and role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon("icons/item.png")
        return super().data(index, role)

    def get_table_name(self, index):
        return self.stringList()[index]