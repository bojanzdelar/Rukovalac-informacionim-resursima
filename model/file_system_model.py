from PySide6 import QtCore, QtWidgets, QtGui
from meta.meta import get_file_display, get_folder_display, file_in_meta, folder_in_meta

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)

        self.setRootPath(root)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        return ""

    def data(self, index, role=QtCore.Qt.DecorationRole):
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            file = self.fileInfo(index)
            name = file.fileName()
            parent_dir = file.dir().dirName()
            if file_in_meta(name, parent_dir):
                return get_file_display(name, parent_dir)
            elif file.isDir() and folder_in_meta(name):
                return get_folder_display(name)
        elif index.column() == 0 and role == QtCore.Qt.DecorationRole:
            file = self.fileInfo(index)
            name = file.fileName()
            if file.isDir():
                if name == "serial":
                    return QtGui.QIcon("icons/serial.png")
                elif name == "sequential":
                    return QtGui.QIcon("icons/sequential.png")
                elif name == "database":
                    return QtGui.QIcon("icons/database.png")
            else:
                return QtGui.QIcon("icons/item.png")
        return super().data(index, role)