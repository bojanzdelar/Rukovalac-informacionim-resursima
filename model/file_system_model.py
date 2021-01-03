from PySide2 import QtCore, QtWidgets, QtGui
from meta.meta import read_meta

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)

        self.meta = read_meta()
        self.setRootPath(root)

    def data(self, index, role=QtCore.Qt.DecorationRole):
        if role == QtCore.Qt.DisplayRole:
            info = self.fileInfo(index)
            name = info.fileName()
            if info.isFile() and name in self.meta:
                return self.meta[info.fileName()]["display"]
        elif role == QtCore.Qt.DecorationRole:
            info = self.fileInfo(index)
            if info.isFile():
                parent_dir = info.dir().dirName()
                if parent_dir == "serial":
                    return QtGui.QIcon("icons/serial.png")
                elif parent_dir == "sequential":
                    return QtGui.QIcon("icons/sequential.png")
        return super().data(index, role)