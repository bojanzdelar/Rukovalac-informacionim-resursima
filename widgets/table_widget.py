from PySide2 import QtCore, QtGui, QtWidgets
from model.serial_file import SerialFile
from model.database import Database
from widgets.tool_bar import ToolBar
from dialog.filter_dialog import FilterDialog
from config.config import read_config

class TableWidget(QtWidgets.QWidget):
    row_selected = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.model = model
        self.information_resource = self.model.information_resource
        self.parent_dir = self.information_resource.get_type()
        self.file_name = self.information_resource.file_name
        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)

        self.generate_layout()

        self.filter_enabled = False
        self.filter_values = [("==", "") for attribute in self.information_resource.get_attribute()]
        self.page_size = read_config()[self.get_type()]
        self.set_page(0)

    def get_type(self):
        return "table_widget"

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()
                
        self.tool_bar = ToolBar(self)
        self.create_tool_bar()
        self.create_table()
        self.current_page = QtWidgets.QLabel("")
        self.create_page_bar()

        layout.addWidget(self.tool_bar, 0, 0)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.current_page, 2, 0, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(self.page_bar, 2, 1, alignment=QtCore.Qt.AlignLeft)

        self.setLayout(layout)
    
    def create_tool_bar(self):
        self.tool_bar.add_filter()
        self.tool_bar.filter_action.triggered.connect(self.filter)
        self.tool_bar.edit_filter_action.triggered.connect(self.filter_dialog)

    def create_page_bar(self):
        self.page_bar = ToolBar(self)
        self.page_bar.add_paging()
        self.page_bar.left_action.triggered.connect(lambda: self.change_page(-1))
        self.page_bar.right_action.triggered.connect(lambda: self.change_page(1))

    def create_table(self):
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.proxy_model)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.table.horizontalHeader().sectionClicked.connect(lambda: self.set_page(self.page))

    def emit_selection(self):
        index = self.table.selectionModel().selectedIndexes()[0]
        self.row_selected.emit(index)

    def filter(self):
        filter_action_position = 5 if self.get_type() == "main_table_widget" else 0

        if self.filter_enabled:
            if isinstance(self. information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.information_resource.data = self.information_resource.read_data()
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[filter_action_position].setIcon(QtGui.QIcon("icons/filter.png"))
        else:
            if isinstance(self.information_resource, SerialFile):
                self.filter_indexes = self.information_resource.filter(self.filter_values)
                for i, index in enumerate(self.filter_indexes):
                    self.filter_indexes[i] = self.proxy_model.mapFromSource(self.model.index(index, 0)).row()
                self.filter_indexes.sort()
            elif isinstance(self.information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.information_resource.filter(self.filter_values)
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[filter_action_position].setIcon(QtGui.QIcon("icons/filter_enabled.png"))

        self.filter_enabled = not self.filter_enabled
        self.set_page(0)

    def refilter(self):
        if self.filter_enabled:
            old_page = self.page
            for i in range(2):
                self.filter()
            self.set_page(old_page)

    def filter_dialog(self):
        dialog = FilterDialog(self.information_resource, self.filter_values)
        dialog.changed.connect(self.change_filter)
        dialog.exec_()

    def change_filter(self, list):
        self.filter_values = list
        self.refilter()

    def set_page(self, page):
        if page < 0 or page > self.total_pages():
            return
        self.page = page
        self.current_page.setText(f"Stranica: {self.page + 1} / {int(self.total_pages()) + 1}")
        self.display_page()

    def total_pages(self):
        if isinstance(self.information_resource, SerialFile) and self.filter_enabled:
            total = (len(self.filter_indexes) - 1) / self.page_size 
        else:
            total = (len(self.information_resource.data) - 1) / self.page_size
        return total if total >= 0 else 0

    def change_page(self, relative_page):
        self.set_page(self.page + relative_page)
    
    def display_page(self):
        index = None
        page_empty = True
        for i in range(self.model.rowCount()):
            self.table.hideRow(i)

        if self.filter_enabled and isinstance(self.information_resource, SerialFile):
            self.filter_indexes = self.information_resource.filter(self.filter_values)
            for i, index in enumerate(self.filter_indexes):
                self.filter_indexes[i] = self.proxy_model.mapFromSource(self.model.index(index, 0)).row()
            self.filter_indexes.sort()
            for i in self.filter_indexes[self.page * self.page_size: (self.page + 1) * self.page_size]:
                self.table.showRow(i)
                page_empty = False

            if len(self.filter_indexes):
                index = self.filter_indexes[0]
        else:
            for i in range(self.page * self.page_size, (self.page + 1) * self.page_size):
                if i >= len(self.model.information_resource.data):
                    break
                self.table.showRow(i)
                page_empty = False

            index = self.page * self.page_size

        self.row_selected.emit(self.proxy_model.index(-1,-1))

        if index is not None:
            self.table.selectRow(index)

            if self.get_type() == "main_table_widget" and not page_empty:
                self.emit_selection()