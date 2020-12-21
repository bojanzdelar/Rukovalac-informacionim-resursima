from PySide2 import QtWidgets, QtCore
from model.file_system_model import FileSystemModel

class DockWidget(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str)

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.model = FileSystemModel(QtCore.QDir.currentPath() + "/data")

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath() + "/data"))
        self.tree.clicked.connect(self.file_clicked)

        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        self.setWidget(self.tree)

    def file_clicked(self, index):
        info = self.model.fileInfo(index)
        if info.isFile():
            self.clicked.emit(self.model.filePath(index))