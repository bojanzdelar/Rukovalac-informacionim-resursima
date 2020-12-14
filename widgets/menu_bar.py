from PySide2 import QtCore, QtWidgets

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.file_menu = self.generate_file_menu()
        self.edit_menu = self.generate_edit_menu()
        self.help_menu = self.generate_help_menu()

    def generate_file_menu(self):
        file_menu = self.addMenu("File")

        save_action = QtWidgets.QAction("Save", self)
        save_all_action = QtWidgets.QAction("Save all", self)
        close_action = QtWidgets.QAction("Close", self)
        close_all_action = QtWidgets.QAction("Close all", self)
        exit_action = QtWidgets.QAction("Exit", self)

        file_menu.addAction(save_action)
        file_menu.addAction(save_all_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)
        file_menu.addAction(close_all_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        return file_menu

    def generate_edit_menu(self):
        edit_menu = self.addMenu("Edit")

        create_action = QtWidgets.QAction("Create", self)
        update_action = QtWidgets.QAction("Update", self)
        delete_action = QtWidgets.QAction("Delete", self)

        edit_menu.addAction(create_action)
        edit_menu.addAction(update_action)
        edit_menu.addAction(delete_action)

        return edit_menu

    def generate_help_menu(self):
        help_menu = self.addMenu("Help")

        manual_action = QtWidgets.QAction("Manual", self)
        about_action = QtWidgets.QAction("About", self)

        help_menu.addAction(manual_action)
        help_menu.addAction(about_action)

        return help_menu