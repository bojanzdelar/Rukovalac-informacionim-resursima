from PySide2 import QtCore, QtGui, QtWidgets
from .menu_bar import MenuBar
from .dock_widget import DockWidget
from .central_widget import CentralWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1280, 960)
        self.setWindowTitle("Rukovalac informacionim resursima")
        self.setWindowIcon(QtGui.QIcon("image/logo-64.png"))

        self.setMenuBar(MenuBar(self))
        self.menuBar().triggered.connect(self.menu_actions)

        self.setStatusBar(QtWidgets.QStatusBar())
        self.statusBar().showMessage("Status bar")
        self.setCentralWidget(CentralWidget(self))
        # self.addToolBar(QtWidgets.QToolBar())

        dock_widget = DockWidget("Informacioni resursi", self)
        dock_widget.clicked.connect(self.centralWidget().add_tab)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)

    def menu_actions(self, action):
        command = action.text()
        if command == "Close":
            self.centralWidget().delete_active_tab()
        elif command == "Close all":
            self.centralWidget().clear()
        elif command == "Save":
            self.centralWidget().currentWidget().information_resource.save_data()
        elif command == "Save all":
            for i in range(self.centralWidget().count()):
                self.centralWidget().widget(i).information_resource.save_data()
        elif command == "Exit":
            self.close()
        elif command == "Create":
            ...
        elif command == "Delete":
            workspace_widget = self.centralWidget().currentWidget()
            if not workspace_widget:
                return
            workspace_widget.delete_row()
        elif command == "Manual":
            ...
        elif command == "About":
            ...