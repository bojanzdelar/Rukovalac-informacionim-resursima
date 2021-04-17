from PySide6 import QtGui, QtWidgets

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.file_menu = self.generate_file_menu()
        self.help_menu = self.generate_help_menu()

    def generate_file_menu(self):
        file_menu = self.addMenu("File")

        save_all_action = QtGui.QAction("Save all", self)
        close_all_action = QtGui.QAction("Close all", self)
        exit_action = QtGui.QAction("Exit", self)

        file_menu.addAction(save_all_action)
        file_menu.addAction(close_all_action)
        file_menu.addAction(exit_action)

        return file_menu

    def generate_help_menu(self):
        help_menu = self.addMenu("Help")

        manual_action = QtGui.QAction("Manual", self)
        about_action = QtGui.QAction("About", self)

        help_menu.addAction(manual_action)
        help_menu.addAction(about_action)

        return help_menu