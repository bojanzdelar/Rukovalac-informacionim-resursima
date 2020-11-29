from PySide2 import QtWidgets, QtGui 

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_table = QtWidgets.QTableWidget()
        self.tab_widget = None
        self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)
        self.show_tabs()
        
    def show_tabs(self):
        self.tab_widget.addTab(QtWidgets.QTableWidget(), "Podtabela 1") 
        self.tab_widget.addTab(QtWidgets.QTableWidget(), "Podtabela 2")
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)