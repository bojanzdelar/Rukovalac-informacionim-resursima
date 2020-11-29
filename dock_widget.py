from PySide2 import QtWidgets, QtCore

class DockWidget(QtWidgets.QDockWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath()))
        self.setWidget(self.tree)