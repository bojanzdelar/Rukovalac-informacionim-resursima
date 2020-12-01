from PySide2 import QtWidgets, QtCore

class DockWidget(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str)

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath() + "/data")

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath() + "/data"))
        self.tree.clicked.connect(self.file_clicked)
        self.setWidget(self.tree)

    def file_clicked(self, index):
        self.clicked.emit(self.model.filePath(index))