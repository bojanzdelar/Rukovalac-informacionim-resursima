from PySide6 import QtWidgets
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.main_table_widget import MainTableWidget
from widgets.table_widget import TableWidget
from widgets.tab_widget import TabWidget
from meta.meta import get_files, get_display

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, name, _type, parent):
        super().__init__(parent)

        self.main_table_widget = MainTableWidget(TableModel(_type, name))
        self.tab_widget = None
        
        if isinstance(self._get_main_inf_res(), (SequentialFile, Database)) and self._get_main_inf_res().meta["children"]:
            self.tab_widget = TabWidget(self)
            self.main_table_widget.row_selected.connect(self.generate_tabs)
        
        if len(self.main_table_widget.model.information_resource.data):
            self.main_table_widget.table.selectRow(0)
            self.generate_tabs(self.main_table_widget.proxy_model.index(0,0))

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.main_table_widget)
        if self.tab_widget:
            main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def _get_main_inf_res(self):
        return self.main_table_widget.model.information_resource

    def generate_tabs(self, index):
        if index.row() < 0 or not self.tab_widget:
            return 
        index = self.main_table_widget.proxy_model.mapToSource(index)
        children = self._get_main_inf_res().get_children(index.row())
        self.tab_widget.generate_tabs(children)