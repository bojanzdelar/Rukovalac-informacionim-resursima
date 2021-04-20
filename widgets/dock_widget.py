from PySide6 import QtWidgets, QtCore
from model.file_system_model import FileSystemModel
from model.database_explorer_model import DatabaseExplorerModel
from config.config import read_config

class DockWidget(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str, str)

    def __init__(self, title, parent):
        super().__init__(title, parent)

        config = read_config()

        self.file_model = FileSystemModel(QtCore.QDir.currentPath() + "/" + config["data"])
        self.file_tree = QtWidgets.QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(QtCore.QDir.currentPath() + "/" + config["data"]))
        self.file_tree.clicked.connect(self.file_clicked)
        self.file_model.directoryLoaded.connect(self.expand)

        for i in range(1, self.file_model.columnCount()):
            self.file_tree.hideColumn(i)

        self.db_model = DatabaseExplorerModel()
        self.db_tree = QtWidgets.QTreeView()
        self.db_tree.setModel(self.db_model)
        self.db_tree.clicked.connect(self.table_clicked)

        multi_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.file_tree)
        layout.addWidget(self.db_tree)
        multi_widget.setLayout(layout)
        self.setWidget(multi_widget)

        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

    def file_clicked(self, index):
        info = self.file_model.fileInfo(index)
        if info.isFile():
            path = self.file_model.filePath(index)
            data_type, data_name = path.split("/")[-2::]
            self.clicked.emit(data_name, data_type)

    def table_clicked(self, index):
        table_name = self.db_model.get_table_name(index.row())
        self.clicked.emit(table_name, "database")

    def expand(self):
        index = self.file_model.index(self.file_model.rootPath())
        for i in range(self.file_model.rowCount(index)):
            child = self.file_model.index(i, 0, index)
            self.file_tree.expand(child)