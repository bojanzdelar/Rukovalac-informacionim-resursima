from PySide2 import QtWidgets
from .workspace_widget import WorkspaceWidget
from meta.meta import read_meta

class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_tab_widget()
        self.open_files = []
        self.meta = read_meta()

    def create_tab_widget(self):
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.delete_tab)

    def tab_name(self, parent_dir, file_name):
        return self.meta[file_name]["display"] + " - " + self.meta[parent_dir]["abbreviation"]
        
    def add_tab(self, path):
        file_name = path.split("/")[-1]
        parent_dir = path.split("/")[-2]
        tab_name = self.tab_name(parent_dir, file_name)
        if tab_name not in self.open_files and file_name in self.meta:
            self.open_files.append(tab_name)
            workspace_widget = WorkspaceWidget(parent_dir, file_name, self)
            workspace_widget.navigate.connect(self.change_tab)
            self.addTab(workspace_widget, tab_name)
    
    def change_tab(self, parent_dir, file_name):
        tab_name = self.tab_name(parent_dir, file_name)
        if tab_name in self.open_files:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela je vec otvorena")
            return
        current_index = self.currentIndex()
        self.delete_tab(current_index)
        self.open_files.append(tab_name)
        workspace_widget = WorkspaceWidget(parent_dir, file_name, self)
        workspace_widget.navigate.connect(self.change_tab)
        self.insertTab(current_index, workspace_widget, tab_name)
        self.setCurrentIndex(current_index)
        
    def delete_tab(self, index):
        self.open_files.remove(self.tabText(index))
        self.removeTab(index)
        
    def delete_all(self):
        self.clear()
        self.open_files = []