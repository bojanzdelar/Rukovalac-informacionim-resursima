from PySide2 import QtWidgets

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.file_menu = self.generate_file_menu()
        self.help_menu = self.generate_help_menu()

    def generate_file_menu(self):
        file_menu = self.addMenu("File")

        save_all_action = QtWidgets.QAction("Save all", self)
        close_all_action = QtWidgets.QAction("Close all", self)
        exit_action = QtWidgets.QAction("Exit", self)

        file_menu.addAction(save_all_action)
        file_menu.addAction(close_all_action)
        file_menu.addAction(exit_action)

        return file_menu

    def generate_help_menu(self):
        help_menu = self.addMenu("Help")

        manual_action = QtWidgets.QAction("Manual", self)
        about_action = QtWidgets.QAction("About", self)

        help_menu.addAction(manual_action)
        help_menu.addAction(about_action)

        return help_menu