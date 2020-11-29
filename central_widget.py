from PySide2 import QtWidgets
from workspace_widget import WorkspaceWidget

class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_tab_widget()
        self.add_tab("Podaci") # FIXME: privremeno

    def create_tab_widget(self):
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.delete_tab)

    def add_tab(self, title = "Naslov"):
        self.addTab(WorkspaceWidget(self), title)
    
    def delete_tab(self, index):
        self.removeTab(index)