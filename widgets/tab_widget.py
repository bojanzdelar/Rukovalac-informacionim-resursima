from PySide6 import QtWidgets
from model.table_model import TableModel
from widgets.entity_widget import EntityWidget
from meta.meta import get_display

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)

    def generate_tabs(self, information_resources):
        self.clear()

        for inf_res in information_resources:
            model = TableModel(inf_res.type)
            model.information_resource = inf_res
            tab = EntityWidget(model, self)
            tab_name = get_display(inf_res.name, inf_res.type)
            self.addTab(tab, tab_name)