from PySide2 import QtCore, QtGui, QtWidgets
from .menu_bar import MenuBar
from .dock_widget import DockWidget
from .central_widget import CentralWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1280, 960)
        self.setWindowTitle("Rukovalac informacionim resursima")
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))

        self.setMenuBar(MenuBar(self))
        self.menuBar().triggered.connect(self.menu_actions)

        self.setStatusBar(QtWidgets.QStatusBar())
        self.statusBar().showMessage("Status bar")
        self.setCentralWidget(CentralWidget(self))

        dock_widget = DockWidget("Informacioni resursi", self)
        dock_widget.clicked.connect(self.centralWidget().add_tab)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)

    def menu_actions(self, action):
        central_widget = self.centralWidget()
        command = action.text()
        if command == "Close all":
            central_widget.delete_all()
        elif command == "Save all":
            for i in range(central_widget.count()):
                central_widget.widget(i).save_table()
        elif command == "Exit":
            self.close()
        elif command == "Manual":
            ...
        elif command == "About":
            ...