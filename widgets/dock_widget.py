from PySide2 import QtWidgets, QtCore
from model.file_system_model import FileSystemModel
from config.config import read_config

class DockWidget(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str)

    def __init__(self, title, parent):
        super().__init__(title, parent)

        config = read_config()

        self.model = FileSystemModel(QtCore.QDir.currentPath() + "/" + config["data"])
        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath() + "/" + config["data"]))
        self.tree.clicked.connect(self.file_clicked)
        self.model.directoryLoaded.connect(self.expand)
        
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        self.setWidget(self.tree)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

    def file_clicked(self, index):
        info = self.model.fileInfo(index)
        if info.isFile():
            self.clicked.emit(self.model.filePath(index))

    def expand(self):
        index = self.model.index(self.model.rootPath())
        for i in range(self.model.rowCount(index)):
            child = index.child(i, 0)
            self.tree.expand(child)