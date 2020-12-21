from PySide2 import QtWidgets
from .workspace_widget import WorkspaceWidget
from meta.meta import read_meta

class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_tab_widget()
        self.open_files = []

    def create_tab_widget(self):
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.delete_tab)

    def add_tab(self, path):
        file_name = path.split("/")[-1]
        meta = read_meta()
        if file_name not in self.open_files and file_name in meta:
            self.open_files.append(file_name)
            self.addTab(WorkspaceWidget(file_name, self), file_name)

    def delete_tab(self, index):
        self.open_files.remove(self.tabText(index))
        self.removeTab(index)
        
    def delete_all(self):
        self.clear()
        self.open_files = []