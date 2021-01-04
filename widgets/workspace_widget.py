from PySide2 import QtCore, QtWidgets, QtGui
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.create_dialog import CreateDialog
from widgets.update_dialog import UpdateDialog
from widgets.filter_dialog import FilterDialog
from widgets.tool_bar import ToolBar
from datetime import datetime
import operator

ops = {
    "=" : operator.eq,
    "!=" : operator.ne,
    "<" : operator.lt,
    "<=" : operator.le,
    ">=" : operator.ge,
    ">" : operator.gt,
    "like" : operator.contains,
}

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent_dir, file_name, parent):
        super().__init__(parent)

        self.parent_dir = parent_dir
        self.file_name = file_name
        self.generate_layout()
        self.filter_enabled = False
        self.filter_values = [("==", "") for attribute in self.information_resource.get_attribute()]

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
        tool_bar.filter_action.triggered.connect(self.filter)
        tool_bar.edit_filter_action.triggered.connect(self.filter_dialog)
        return tool_bar

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        return table

    def create_main_table(self):
        self.model = TableModel(self.parent_dir, self.file_name)
        self.information_resource = self.model.information_resource
        main_table = self.create_table()
        main_table.setModel(self.model)
        main_table.clicked.connect(self.selected_row)
        return main_table

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
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.delete_element(indexes[0].row())
        self.model.layoutChanged.emit()
        self.main_table.clearSelection()
        self.tab_widget.clear()
        self.refilter()

    def selected_row(self, index):
        if not isinstance(self.information_resource, (SequentialFile, Database)):
            return

        children = self.information_resource.get_children(index.row())
        self.tab_widget.clear() 
        for table in children:
            model = TableModel(self.parent_dir)
            model.information_resource = table
            tab = self.create_table(self.tab_widget)
            tab.setModel(model)
            self.tab_widget.addTab(tab, table.file_name) 

    def save_table(self):
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.save_data()
        self.model.layoutChanged.emit()

    def filter(self):
        self.filter_show() if self.filter_enabled else self.filter_hide()
        self.filter_enabled = not self.filter_enabled

    def filter_show(self):
        for i in range(self.model.rowCount()):
            self.main_table.showRow(i)
        self.tool_bar.actions()[5].setIcon(QtGui.QIcon("icons/filter.png"))

    def filter_hide(self):
        for i in range(self.model.rowCount()):
            element = self.information_resource.read_element(i).copy()
            match_filter = True
            for j in range(len(element)):
                operator, text = self.filter_values[j]
                input_type = self.information_resource.get_attribute(j)["input"]
                if (text == "") or (input_type == "date" and text == "01/01/1900"):
                    continue
                if input_type == "date":
                    text = datetime.strptime(text, "%d/%m/%Y")
                    element[j] = datetime.strptime(str(element[j]), "%d/%m/%Y")
                if (operator == "not like" and ops["like"](element[j], text)) \
                        or (operator != "not like" and not ops[operator](element[j], text)):
                    match_filter = False
                    break
            if not match_filter:
                self.main_table.hideRow(i)
        self.tool_bar.actions()[5].setIcon(QtGui.QIcon("icons/filter_enabled.png"))

    def refilter(self):
        if self.filter_enabled:
            self.filter_show()
            self.filter_hide()

    def filter_dialog(self):
        dialog = FilterDialog(self.information_resource, self.filter_values)
        dialog.changed.connect(self.change_filter)
        dialog.exec_()

    def change_filter(self, list):
        self.filter_values = list
        self.refilter()