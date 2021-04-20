from PySide6 import QtGui, QtWidgets

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        
    def add_crud(self):
        self.create_action = self.addAction(QtGui.QIcon("icons/create.png"), "Create")
        self.update_action = self.addAction(QtGui.QIcon("icons/update.png"), "Update")
        self.delete_action = self.addAction(QtGui.QIcon("icons/delete.png"), "Delete")
        self.save_action = self.addAction(QtGui.QIcon("icons/save.png"), "Save")

    def add_filter(self):
        self.filter_action = self.addAction(QtGui.QIcon("icons/filter.png"), "Filter")
        self.edit_filter_action = self.addAction(QtGui.QIcon("icons/settings.png"), "Edit filter")
 
    def add_split_merge(self):
        self.addSeparator()
        self.split_action = self.addAction(QtGui.QIcon("icons/split.png"), "Split")
        self.merge_action = self.addAction(QtGui.QIcon("icons/merge.png"), "Merge")

    def add_navigation(self):
        self.addSeparator()
        self.parent_action = self.addAction(QtGui.QIcon("icons/up.png"), "Parent")
        self.child_action = self.addAction(QtGui.QIcon("icons/down.png"), "Child")
