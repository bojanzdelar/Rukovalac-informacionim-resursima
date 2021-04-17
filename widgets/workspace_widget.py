from PySide6 import QtWidgets
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.main_table_widget import MainTableWidget
from widgets.table_widget import TableWidget
from meta.meta import get_files, get_file_display

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent_dir, file_name, parent):
        super().__init__(parent)

        self.parent_dir = parent_dir
        self.file_name = file_name

        self.generate_layout()    

    def generate_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_model = TableModel(self.parent_dir, self.file_name)
        self.main_information_resource = self.main_model.information_resource
        self.main_table_widget = MainTableWidget(self.main_model)
        self.main_table_widget.row_selected.connect(self.selected_row)
        self.main_table_widget.clear_tab_widget.connect(self.clear_tab_widget)

        self.main_layout.addWidget(self.main_table_widget)
        
        self.tab_widget = None
        if isinstance(self.main_information_resource, (SequentialFile, Database)) \
                and self.main_information_resource.meta["children"]:
            self.create_tab_widget()
            self.main_layout.addWidget(self.tab_widget)

        if len(self.main_information_resource.data):
            self.main_table_widget.table.selectRow(0)
            self.selected_row(self.main_table_widget.proxy_model.index(0,0))
            
        self.setLayout(self.main_layout)

    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def clear_tab_widget(self):
        if not self.tab_widget:
            return
        self.tab_widget.clear()

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)
    
    def selected_row(self, index):
        if not isinstance(self.main_information_resource, (SequentialFile, Database)) \
                or not self.main_information_resource.meta["children"]:
            return

        self.tab_widget.clear()
        if index.row() < 0:
            return 
        index = self.main_table_widget.proxy_model.mapToSource(index)
        children = self.main_information_resource.get_children(index.row())
        for table in children:
            model = TableModel(self.parent_dir)
            model.information_resource = table
            tab = TableWidget(model, self.tab_widget)
            tab_name = get_file_display(table.file_name, self.parent_dir)
            self.tab_widget.addTab(tab, tab_name)