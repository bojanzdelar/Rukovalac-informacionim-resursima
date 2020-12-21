from PySide2 import QtCore, QtWidgets, QtGui
from model.table_model import TableModel
from widgets.create_dialog import CreateDialog
from widgets.update_dialog import UpdateDialog
from widgets.filter_dialog import FilterDialog
from widgets.tool_bar import ToolBar

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, file_name, parent):
        super().__init__(parent)

        self.file_name = file_name
        self.filter_enabled = False
        self.filter_attribute = 0
        self.filter_text = ""

        self.generate_layout()

    def generate_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.tool_bar = self.create_tool_bar()
        self.main_table = self.create_main_table()
        self.tab_widget = self.create_tab_widget()
        self.main_layout.addWidget(self.tool_bar)
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def create_tool_bar(self):
        tool_bar = ToolBar(self)
        tool_bar.create_action.triggered.connect(self.create_row)
        tool_bar.update_action.triggered.connect(self.update_row)
        tool_bar.delete_action.triggered.connect(self.delete_row)
        tool_bar.save_action.triggered.connect(self.save_table)
        tool_bar.sort_action.triggered.connect(self.sort)
        tool_bar.filter_action.triggered.connect(self.filter)
        tool_bar.edit_filter_action.triggered.connect(self.filter_dialog)
        return tool_bar

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return table

    def create_main_table(self):
        self.model = TableModel(self.file_name)
        self.information_resource = self.model.information_resource
        main_table = self.create_table()
        main_table.setModel(self.model)
        main_table.clicked.connect(self.selected)
        return main_table

    def selected(self, index):
        children = self.information_resource.get_children()
        self.tab_widget.clear()
        for file_name, attributes in children.items():
            model = TableModel(file_name)
            main_attributes = self.information_resource.get_primary_key()
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
        self.refilter()

    def update_row(self):
        indexes = self.main_table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        self.model.layoutAboutToBeChanged.emit()
        dialog = UpdateDialog(self.information_resource, indexes[0].row())
        dialog.exec_() 
        self.model.layoutChanged.emit()
        self.refilter()

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def delete_row(self):
        indexes = self.main_table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        index = indexes[0].row()
        if self.information_resource.restrict_remove(index):
            QtWidgets.QMessageBox.warning(self, "Greska", "Ne mozete da obrisete entitet" 
                + " cije se vrednosti primarnog kljuca koriste kao strani kljuc u child tabelama")
            return
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.delete_element(indexes[0].row())
        self.model.layoutChanged.emit()
        self.main_table.clearSelection()
        self.tab_widget.clear()
        self.refilter()

    def save_table(self):
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.save_data()
        self.model.layoutChanged.emit()

    def sort(self):
        self.model.layoutAboutToBeChanged.emit()
        if not self.information_resource.sort():
            QtWidgets.QMessageBox.warning(self, "Greska", 
                "Ne mozete da sortirate tabelu koja nema primarni kljuc")
        self.model.layoutChanged.emit()

    def filter(self):
        self.filter_show() if self.filter_enabled else self.filter_hide()
        self.filter_enabled = not self.filter_enabled

    def filter_show(self):
        for i in range(self.model.rowCount()):
            self.main_table.showRow(i)
        self.tool_bar.actions()[6].setIcon(QtGui.QIcon("icons/filter.png"))

    def filter_hide(self):
        for i in range(self.model.rowCount()):
            element = self.information_resource.read_element(i)
            if self.filter_text.lower() not in element[self.filter_attribute].lower():
                self.main_table.hideRow(i)
        self.tool_bar.actions()[6].setIcon(QtGui.QIcon("icons/filter_enabled.png"))

    def refilter(self):
        if self.filter_enabled:
            self.filter_hide()

    def filter_dialog(self):
        dialog = FilterDialog(self.information_resource, self.filter_attribute, self.filter_text)
        dialog.changed.connect(self.change_filter)
        dialog.exec_()

    def change_filter(self, list):
        self.filter_attribute = list[0]
        self.filter_text = list[1]
        self.refilter()