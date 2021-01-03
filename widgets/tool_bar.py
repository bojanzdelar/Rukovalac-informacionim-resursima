from PySide2 import QtGui, QtWidgets

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_actions()

    def add_actions(self):
        self.create_action = self.addAction(QtGui.QIcon("icons/create.png"), "Create")
        self.update_action = self.addAction(QtGui.QIcon("icons/update.png"), "Update")
        self.delete_action = self.addAction(QtGui.QIcon("icons/delete.png"), "Delete")
        self.save_action = self.addAction(QtGui.QIcon("icons/save.png"), "Save")
        self.addSeparator()
        self.filter_action = self.addAction(QtGui.QIcon("icons/filter.png"), "Filter")
        self.edit_filter_action = self.addAction(QtGui.QIcon("icons/settings.png"), "Edit filter")