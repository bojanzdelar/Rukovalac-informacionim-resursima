from PySide2 import QtCore, QtWidgets, QtGui
from meta.meta import read_meta

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)

        self.meta = read_meta()
        self.setRootPath(root)

    def data(self, index, role=QtCore.Qt.DecorationRole):
        if role == QtCore.Qt.DisplayRole:
            file = self.fileInfo(index)
            if file.fileName() in self.meta:
                return self.meta[file.fileName()]["display"]
        elif role == QtCore.Qt.DecorationRole:
            file = self.fileInfo(index)
            name = file.fileName()
            if file.isDir():
                if name == "serial":
                    return QtGui.QIcon("icons/serial.png")
                elif name == "sequential":
                    return QtGui.QIcon("icons/sequential.png")
                elif name == "database":
                    return QtGui.QIcon("icons/database.png")
            return QtGui.QIcon("icons/item.png")
        return super().data(index, role)