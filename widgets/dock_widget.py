from PySide6 import QtWidgets, QtCore
from model.file_system_model import FileSystemModel
from model.database_explorer_model import DatabaseExplorerModel
from config.config import read_config

class DockWidget(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str, str)

    def __init__(self, title, parent):
        super().__init__(title, parent)

        config = read_config()
        self.fs_model = FileSystemModel(QtCore.QDir.currentPath() + "/" + config["data"])
        self.file_tree = QtWidgets.QTreeView()
        self.file_tree.setModel(self.fs_model)
        self.file_tree.setRootIndex(self.fs_model.index(QtCore.QDir.currentPath() + "/" + config["data"]))
        self.file_tree.clicked.connect(self.file_clicked)
        self.fs_model.directoryLoaded.connect(lambda: self.file_tree.expandAll())
        for i in range(1, self.fs_model.columnCount()):
            self.file_tree.hideColumn(i)

        self.dbe_model = DatabaseExplorerModel()
        self.db_tree = QtWidgets.QTreeView()
        self.db_tree.setModel(self.dbe_model)
        self.db_tree.clicked.connect(self.table_clicked)

        multi_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.file_tree)
        layout.addWidget(self.db_tree)
        multi_widget.setLayout(layout)
        self.setWidget(multi_widget)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

    def file_clicked(self, index):
        info = self.fs_model.fileInfo(index)
        if info.isFile():
            path = self.fs_model.filePath(index)
            data_type, data_name = path.split("/")[-2::]
            self.clicked.emit(data_name, data_type)

    def table_clicked(self, index):
        table_name = self.dbe_model.get_table_name(index.row())
        self.clicked.emit(table_name, "database")