from PySide2 import QtWidgets, QtGui
from model.model import Model
from widgets.create_dialog import CreateDialog

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
        self.model = Model(self.file_name)
        self.information_resource = self.model.information_resource
        main_table = self.create_table()
        main_table.setModel(self.model)
        main_table.clicked.connect(self.selected)
        return main_table

    def selected(self, index):
        relations = self.information_resource.get_relations()
        self.tab_widget.clear()
        for file_name, attributes in relations.items():
            model = Model(file_name)
            main_attributes = self.information_resource.meta["primary key"]
            main_attributes_indexes = self.information_resource.get_attributes_indexes(main_attributes)
            values = []
            for attr_index in main_attributes_indexes:
                values.append(self.model.get_element(index)[attr_index])
            model.information_resource.filter(attributes, values)
            tab = self.create_table(self.tab_widget)
            tab.setModel(model)
            self.tab_widget.addTab(tab, file_name)

    def create_tab_widget(self):
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.delete_tab)
        return tab_widget

    def create_row(self):
        self.model.layoutAboutToBeChanged.emit()
        dialog = CreateDialog(self.information_resource)
        dialog.exec_()
        self.model.layoutChanged.emit()

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def delete_row(self):
        indexes = self.main_table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.delete_element(indexes[0].row())
        self.model.layoutChanged.emit()
        self.main_table.clearSelection()
        self.tab_widget.clear()