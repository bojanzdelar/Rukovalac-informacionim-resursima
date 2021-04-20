from PySide6 import QtWidgets
from .workspace_widget import WorkspaceWidget
from meta.meta import get_tab_name, is_in_meta

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)

    @property
    def tabs(self):
        tabs_list = []
        for i in range(self.count()):
            tabs_list.append(self.tabText(i))
        return tabs_list

    def get_index(self, tab_name):
        return self.tabs.index(tab_name)
        
    def add_tab(self, data_name, data_type):
        tab_name = get_tab_name(data_name, data_type)
        if tab_name not in self.tabs and is_in_meta(data_name, data_type):
            workspace_widget = WorkspaceWidget(data_type, data_name, self)
            workspace_widget.main_table_widget.change_table.connect(self.change_tab)
            workspace_widget.main_table_widget.close_tab.connect(self.remove_tab)
            self.addTab(workspace_widget, tab_name)
            self.setCurrentIndex(self.currentIndex() + 1)
        else:
            index = self.get_index(tab_name)
            self.setCurrentIndex(index)
        
    def change_tab(self, data_type, data_name):
        tab_name = get_tab_name(data_name, data_type)
        if tab_name in self.tabs:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela je vec otvorena")
            return
        workspace_widget = WorkspaceWidget(data_type, data_name, self)
        workspace_widget.main_table_widget.change_table.connect(self.change_tab)
        workspace_widget.main_table_widget.close_tab.connect(self.remove_tab)
        current_index = self.currentIndex()
        self.removeTab(current_index)
        self.insertTab(current_index, workspace_widget, tab_name)
        self.setCurrentIndex(current_index)

    def remove_tab(self, tab_name):
        index = self.get_index(tab_name)
        if index is None:
            return
        self.removeTab(index)    