from PySide2 import QtCore, QtWidgets, QtGui
import json

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)

        self.meta = self.read_meta()
        self.setRootPath(root)

    def read_meta(self):
        with open("meta.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def data(self, index, role=QtCore.Qt.DecorationRole):
        if role == QtCore.Qt.DisplayRole:
            info = self.fileInfo(index)
            if info.isFile():
                return self.meta[info.fileName()]["display"]
        elif role == QtCore.Qt.DecorationRole:
            info = self.fileInfo(index)
            name = info.fileName()
            if info.isFile():
                if name.endswith("ser.csv"):
                    return QtGui.QIcon("icons/serial.png")
                elif name.endswith("sek.csv"):
                    return QtGui.QIcon("icons/sequential.png")
        return super().data(index, role)