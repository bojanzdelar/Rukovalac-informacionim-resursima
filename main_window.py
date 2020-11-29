from PySide2 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(640, 480)
        self.setWindowTitle("Rukovalac informacionim resursima")
        self.setWindowIcon(QtGui.QIcon("logo.png"))

        self.setMenuBar(QtWidgets.QMenuBar())
        self.setStatusBar(QtWidgets.QStatusBar())
        self.statusBar().showMessage("Status bar")
        self.setCentralWidget(QtWidgets.QTabWidget())
        self.addToolBar(QtWidgets.QToolBar())
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, QtWidgets.QDockWidget("Dock widget"))
