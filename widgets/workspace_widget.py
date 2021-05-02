from PySide6 import QtWidgets
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.main_entity_widget import MainEntityWidget
from widgets.entity_widget import EntityWidget
from widgets.tab_widget import TabWidget
from meta.meta import get_files, get_display

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, name, _type, parent):
        super().__init__(parent)

        self.main_entity_widget = MainEntityWidget(TableModel(_type, name))
        self.tab_widget = None
        
        if isinstance(self.main_entity_widget.model.information_resource, (SequentialFile, Database)) \
                and self.main_entity_widget.model.information_resource.meta["children"]:
            self.tab_widget = TabWidget(self)
            self.main_entity_widget.table_view.row_selected.connect(self.row_selected)
        
        if len(self.main_entity_widget.model.information_resource.data):
            self.main_entity_widget.table_view.selectRow(0)
            self.row_selected(self.main_entity_widget.table_view.proxy_model.index(0,0))

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.main_entity_widget)
        if self.tab_widget:
            main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def row_selected(self, index):
        if index.row() < 0 or not self.tab_widget:
            return 
        index = self.main_entity_widget.table_view.proxy_model.mapToSource(index)
        children = self.main_entity_widget.model.information_resource.get_children(index.row())
        self.tab_widget.generate_tabs(children)