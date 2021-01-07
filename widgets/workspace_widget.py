from PySide2 import QtCore, QtWidgets, QtGui
from model.serial_file import SerialFile
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.create_dialog import CreateDialog
from widgets.update_dialog import UpdateDialog
from widgets.filter_dialog import FilterDialog
from widgets.navigation_dialog import NavigationDialog
from widgets.tool_bar import ToolBar
from meta.meta import read_meta

class WorkspaceWidget(QtWidgets.QWidget):
    navigate = QtCore.Signal(str, str)

    def __init__(self, parent_dir, file_name, parent):
        super().__init__(parent)

        self.parent_dir = parent_dir
        self.file_name = file_name
        self.meta = read_meta()
        self.generate_layout()
        self.filter_enabled = False
        self.filter_values = [("==", "") for attribute in self.information_resource.get_attribute()]

    def generate_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = self.create_tab_widget()
        self.main_table = self.create_main_table()
        self.tool_bar = self.create_tool_bar()
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
        tool_bar.filter_action.triggered.connect(self.filter)
        tool_bar.edit_filter_action.triggered.connect(self.filter_dialog)
        if isinstance(self.information_resource, (SequentialFile, Database)):
            tool_bar.add_navigation()
            tool_bar.parent_action.triggered.connect(self.parent)
            tool_bar.child_action.triggered.connect(self.child)
            tool_bar.left_action.triggered.connect(lambda: self.move(-1))
            tool_bar.right_action.triggered.connect(lambda: self.move(1))
        return tool_bar

    def create_tab_widget(self):
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.delete_tab)
        return tab_widget

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        return table

    def create_main_table(self):
        self.model = TableModel(self.parent_dir, self.file_name)
        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.information_resource = self.model.information_resource
        main_table = self.create_table()
        main_table.setModel(self.proxy_model)
        main_table.clicked.connect(self.selected_row)
        main_table.setSortingEnabled(True)
        main_table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        if len(self.information_resource.data):
            main_table.selectRow(0)
            self.selected_row(self.proxy_model.index(0,0))
        return main_table

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
        index = self.proxy_model.mapToSource(indexes[0])
        self.model.layoutAboutToBeChanged.emit()
        dialog = UpdateDialog(self.information_resource, index.row())
        dialog.exec_() 
        self.model.layoutChanged.emit()
        self.refilter()

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def delete_row(self):
        indexes = self.main_table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        index = self.proxy_model.mapToSource(indexes[0])
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.delete_element(index.row())
        self.model.layoutChanged.emit()
        self.main_table.clearSelection()
        self.tab_widget.clear()
        self.refilter()

    def selected_row(self, index):
        if not isinstance(self.information_resource, (SequentialFile, Database)):
            return
        index = self.proxy_model.mapToSource(index)
        children = self.information_resource.get_children(index.row())
        self.tab_widget.clear() 
        for table in children:
            model = TableModel(self.parent_dir)
            model.information_resource = table
            tab = self.create_table(self.tab_widget)
            tab.setModel(model)
            tab_name = self.meta[table.file_name]["display"]
            self.tab_widget.addTab(tab, tab_name) 

    def save_table(self):
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.save_data()
        self.model.layoutChanged.emit()

    def filter(self):
        if self.filter_enabled:
            if isinstance(self.information_resource, SerialFile):
                for i in range(self.model.rowCount()):
                    self.main_table.showRow(i)
            elif isinstance(self. information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.information_resource.data = self.information_resource.read_data()
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[5].setIcon(QtGui.QIcon("icons/filter.png"))
        else:
            if isinstance(self.information_resource, SerialFile):
                for i in self.information_resource.filter(self.filter_values):
                    self.main_table.hideRow(i)
            elif isinstance(self.information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.information_resource.filter(self.filter_values)
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[5].setIcon(QtGui.QIcon("icons/filter_enabled.png"))

        self.filter_enabled = not self.filter_enabled

    def refilter(self):
        for i in range(2):
            self.filter()

    def filter_dialog(self):
        dialog = FilterDialog(self.information_resource, self.filter_values)
        dialog.changed.connect(self.change_filter)
        dialog.exec_()

    def change_filter(self, list):
        self.filter_values = list
        self.refilter()

    def parent(self):
        parents = self.information_resource.get_parents()
        if not parents:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela nema parent tabele")
            return
        tables = {}
        for parent in parents:
            tables[self.meta[parent]["display"]] = parent
        dialog = NavigationDialog(tables)
        dialog.selected.connect(self.change_table)
        dialog.exec_()

    def child(self):
        children = self.information_resource.meta["children"]
        if not children:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela nema child tabele")
            return
        tables = {}
        for child in children:
            tables[self.meta[child]["display"]] = child
        dialog = NavigationDialog(tables)
        dialog.selected.connect(self.change_table)
        dialog.exec_()

    def change_table(self, table_name):
        self.navigate.emit(self.parent_dir, table_name)

    def move(self, relative_index):
        self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex() + relative_index)

    