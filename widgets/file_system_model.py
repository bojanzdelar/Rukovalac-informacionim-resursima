from PySide2 import QtCore, QtWidgets, QtGui

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)

        self.setRootPath(root)

    def data(self, index, role=QtCore.Qt.DecorationRole):
        if role == QtCore.Qt.DecorationRole:
            info = self.fileInfo(index)
            if info.isFile():
                name = info.fileName()
                if "ser.csv" in name:
                    return QtGui.QIcon("icons/serial.png")
                elif "sek.csv" in name:
                    return QtGui.QIcon("icons/sequential.png")
        return super().data(index, role)