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
        relations = self.main_table.model().information_resource.get_relations()
        self.tab_widget.clear()
        for relation, link in relations.items():
            model = Model(relation)
            attribute_index = self.main_table.model().information_resource.get_attribute_index(link[0])
            value = self.main_table.model().get_element(index)[attribute_index]
            model.information_resource.filter(link[1], value)
            tab = self.create_table(self.tab_widget)
            tab.setModel(model)
            self.tab_widget.addTab(tab, relation)

    def create_tab_widget(self):
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.delete_tab)
        return tab_widget
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)