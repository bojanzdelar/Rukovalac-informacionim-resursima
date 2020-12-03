from PySide2 import QtWidgets, QtGui
from model.model import Model

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, file_name, parent):
        super().__init__(parent)

        self.file_name = file_name
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_table = self.create_main_table()
        self.tab_widget = self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return table

    def create_main_table(self):
        model = Model(self.file_name)
        main_table = self.create_table()
        main_table.setModel(model)
        main_table.clicked.connect(self.selected)
        return main_table

    def selected(self, index):
        subtables = self.main_table.model().get_subtables()
        self.tab_widget.clear()
        for subtable in subtables:
            selected_element = self.main_table.model().get_element(index)
            submodel = Model(subtable)
            submodel.list = selected_element.list
            tab = self.create_table(self.tab_widget)
            tab.setModel(submodel)
            self.tab_widget.addTab(tab, subtable)

    def create_tab_widget(self):
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.delete_tab)
        return tab_widget
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)