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

        self.setCentralWidget(CentralWidget(self))

        self.setStatusBar(QtWidgets.QStatusBar())

        self.timer= QtCore.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        dock_widget = DockWidget("Datoteke", self)
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
            QtWidgets.QMessageBox.information(self, "Manual", "Uputstvo za upotrebu programa Rukovalac informacionim resursima"
                + " mozete preuzeti na internet stranici www.infhandler.com/rs")
        elif command == "About":
            QtWidgets.QMessageBox.information(self, "About", "Program Rukovalac informacionim resursima je realizovan " 
                + " u sklopu projekta iz predmeta Baze podataka. Autor je Bojan Zdelar, ciji je broj indeksa 2019/270983")

    def show_time(self):
        time = QtCore.QDateTime.currentDateTime()
        time_display = time.toString('hh:mm:ss, dd/MM/yyyy')
        self.statusBar().showMessage(time_display)