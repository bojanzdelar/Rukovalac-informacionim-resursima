from PySide6 import QtCore, QtGui, QtWidgets
from widgets.menu_bar import MenuBar
from widgets.dock_widget import DockWidget
from widgets.central_widget import CentralWidget
from widgets.status_bar import StatusBar

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1280, 960)
        self.setWindowTitle("Rukovalac informacionim resursima")
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))

        self.setCentralWidget(CentralWidget(self))

        self.setMenuBar(MenuBar(self))
        self.menuBar().close_all.connect(self.centralWidget().clear)
        self.menuBar().save_all.connect(self.centralWidget().save_all)
        self.menuBar().exit.connect(self.close)

        dock_widget = DockWidget("Informacioni resursi", self)
        dock_widget.clicked.connect(self.centralWidget().add_tab)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)

        self.setStatusBar(StatusBar(self))