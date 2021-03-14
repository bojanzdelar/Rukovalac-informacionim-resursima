from PySide2 import QtCore, QtWidgets
from model.serial_file import SerialFile
from model.sequential_file import SequentialFile
from model.database import Database
from model.table_model import TableModel
from widgets.table_widget import TableWidget
from dialog.create_dialog import CreateDialog
from dialog.update_dialog import UpdateDialog
from dialog.navigation_dialog import NavigationDialog
from dialog.split_dialog import SplitDialog
from dialog.merge_dialog import MergeDialog
from meta.meta import get_files, get_file_display, get_file_tab_name, same_file_meta, remove_file
from config.config import read_config
import os

class MainTableWidget(TableWidget):
    change_table = QtCore.Signal(str, str)
    close_tab = QtCore.Signal(str)
    clear_tab_widget = QtCore.Signal()

    def __init__(self, model, parent=None):
        super().__init__(model, parent)
        
    def get_type(self):
        return "main_table_widget"

    def create_table(self):
        super().create_table()

        self.table.clicked.connect(self.emit_selection)

    def create_tool_bar(self):
        self.tool_bar.add_crud()        
        self.tool_bar.create_action.triggered.connect(self.create_row)
        self.tool_bar.update_action.triggered.connect(self.update_row)
        self.tool_bar.delete_action.triggered.connect(self.delete_row)
        self.tool_bar.save_action.triggered.connect(self.save_table)
        
        self.tool_bar.addSeparator()
        super().create_tool_bar()

        if isinstance(self.information_resource, (SequentialFile, Database)):
            self.tool_bar.add_navigation()
            self.tool_bar.parent_action.triggered.connect(self.parent)
            self.tool_bar.child_action.triggered.connect(self.child)
        if isinstance(self.information_resource, SerialFile):
            self.tool_bar.add_split_merge()
            self.tool_bar.split_action.triggered.connect(self.split)
            self.tool_bar.merge_action.triggered.connect(self.merge)

    def create_row(self):
        self.model.layoutAboutToBeChanged.emit()
        dialog = CreateDialog(self.information_resource)
        dialog.created.connect(self.created)
        dialog.exec_()
        self.model.layoutChanged.emit()
        self.refilter()

    def created(self):
        self.model.layoutChanged.emit()
        self.refilter()
        self.model.layoutAboutToBeChanged.emit()

    def update_row(self):
        indexes = self.table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        index = self.proxy_model.mapToSource(indexes[0])
        self.model.layoutAboutToBeChanged.emit()
        dialog = UpdateDialog(self.information_resource, index.row())
        dialog.exec_() 
        self.model.layoutChanged.emit()
        self.refilter()

    def delete_row(self):
        indexes = self.table.selectionModel().selectedIndexes()
        if not len(indexes):
            return
        index = self.proxy_model.mapToSource(indexes[0])
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.delete_element(index.row())
        self.model.layoutChanged.emit()
        self.table.clearSelection()
        self.clear_tab_widget.emit()
        self.refilter()

    def save_table(self):
        self.model.layoutAboutToBeChanged.emit()
        self.information_resource.save_data()
        self.model.layoutChanged.emit()

    def split(self):
        dialog = SplitDialog(self.information_resource)
        dialog.selected.connect(self.information_resource.split)
        accepted = dialog.exec_()

        if accepted:
            self.close_file(self.file_name, "split")

    def merge(self):
        file_organization = self.information_resource.get_type()
        files = os.listdir(read_config()[file_organization])
        files = [file for file in files \
            if same_file_meta(self.file_name, file, file_organization) and self.file_name != file]
        if not files:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela nema tabelu s kojom bi mogla da se spoji")
            return

        dialog = MergeDialog(self.information_resource, files)
        dialog.selected.connect(self.information_resource.merge)
        dialog.merged.connect(self.close_file)
        accepted = dialog.exec_()

        if accepted:
            # Other file will be closed when signal gets emitted
            self.close_file(self.file_name, "merge")

    def merge_completed(self, file_name):
        self.merged_file_name = file_name

    def close_file(self, file_name, mode):
        tab_name = get_file_tab_name(file_name, self.parent_dir)
        if mode == "split" or (mode == "merge" and self.information_resource.merged_file_name != file_name):
            remove_file(file_name, self.parent_dir)
        self.close_tab.emit(tab_name)

    def parent(self):
        parent_types = self.information_resource.get_parents()
        parent_files = []
        for type in parent_types:
            parent_files += get_files(type, self.parent_dir)
        if not parent_files:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela nema parent tabele")
            return
        tables = {}
        for parent in parent_files:
            tables[get_file_display(parent, self.parent_dir)] = parent
        dialog = NavigationDialog(tables)
        dialog.selected.connect(self.new_table)
        dialog.exec_()

    def child(self):
        children_types = self.information_resource.meta["children"]
        children_files = []
        for type in children_types:
            children_files += get_files(type, self.parent_dir)
        if not children_files:
            QtWidgets.QMessageBox.warning(None, "Greska", "Izabrana tabela nema child tabele")
            return
        tables = {}
        for child in children_files:
            tables[get_file_display(child, self.parent_dir)] = child
        dialog = NavigationDialog(tables)
        dialog.selected.connect(self.new_table)
        dialog.exec_()

    def new_table(self, table_name):
        self.change_table.emit(self.parent_dir, table_name)