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
        central_widget = self.centralWidget()
        command = action.text()
        if command == "Close":
            central_widget.delete_active_tab()
        elif command == "Close all":
            central_widget.clear()
        elif command == "Save":
            central_widget.currentWidget().information_resource.save_data()
        elif command == "Save all":
            for i in range(central_widget.count()):
                central_widget.widget(i).information_resource.save_data()
        elif command == "Exit":
            self.close()
        elif command == "Create":
            workspace_widget = central_widget.currentWidget()
            if not workspace_widget:
                return
            workspace_widget.create_row()
        elif command == "Update":
            workspace_widget = central_widget.currentWidget()
            if not workspace_widget:
                return
            workspace_widget.update_row()
        elif command == "Delete":
            workspace_widget = central_widget.currentWidget()
            if not workspace_widget:
                return
            workspace_widget.delete_row()
        elif command == "Manual":
            ...
        elif command == "About":
            ...