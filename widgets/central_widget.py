from PySide2 import QtWidgets
from .workspace_widget import WorkspaceWidget

class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_tab_widget()

    def create_tab_widget(self):
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.delete_tab)

    def add_tab(self, path):
        file_name = path.split("/")[-1]
        self.addTab(WorkspaceWidget(file_name, self), file_name)

    def delete_tab(self, index):
        self.removeTab(index)

    def delete_active_tab(self):
        self.removeTab(self.currentIndex())