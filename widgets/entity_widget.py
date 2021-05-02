from PySide6 import QtCore, QtGui, QtWidgets
from model.serial_file import SerialFile
from model.database import Database
from widgets.table_view import TableView
from widgets.tool_bar import ToolBar
from widgets.pagination_bar import PaginationBar
from dialog.filter_dialog import FilterDialog
from config.config import read_config

class EntityWidget(QtWidgets.QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.model = model

        self.filter_values = [("==", "") for attribute in self.model.information_resource.get_attribute()]

        self.table_view = TableView(model, self)
        
        self.tool_bar = ToolBar(self)
        self.tool_bar.add_filter()
        self.tool_bar.filter_action.triggered.connect(self.table_view.filter)
        self.tool_bar.edit_filter_action.triggered.connect(self.filter_dialog)

        page_size = read_config()["page_size"]
        self.pagination_bar = PaginationBar(page_size, self.total_pages(page_size), self)


        self.table_view.set_page.connect(self.pagination_bar.set_page)
        self.pagination_bar.display_page.connect(self.table_view.display_page)

        print(page_size)
        self.table_view.display_page(0, page_size) # FIXME: UGH    

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.table_view)
        layout.addWidget(self.pagination_bar)
        self.setLayout(layout)

    def filter_dialog(self):
        dialog = FilterDialog(self.model.information_resource, self.filter_values)
        dialog.changed.connect(self.change_filter)
        dialog.exec_()

    def change_filter(self, list):
        self.filter_values = list
        self.table_view.refilter()
    
    def total_pages(self, page_size):
        if isinstance(self.model.information_resource, SerialFile) and self.table_view.filtered:
            total = (len(self.filter_indexes) - 1) / page_size 
        else:
            total = (len(self.model.information_resource.data) - 1) / page_size
        return total if total >= 0 else 0