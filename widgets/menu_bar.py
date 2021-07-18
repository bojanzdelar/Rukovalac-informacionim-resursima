from PySide6 import QtCore, QtGui, QtWidgets

class MenuBar(QtWidgets.QMenuBar):
    close_all = QtCore.Signal()
    save_all = QtCore.Signal()
    exit = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        
        self.file_menu = self.addMenu("File")
        self.file_menu.addAction(QtGui.QAction("Save all", self))
        self.file_menu.addAction(QtGui.QAction("Close all", self))
        self.file_menu.addAction(QtGui.QAction("Exit", self))

        self.help_menu = self.addMenu("Help")
        self.help_menu.addAction(QtGui.QAction("Manual", self))
        self.help_menu.addAction(QtGui.QAction("About", self))

        self.triggered.connect(self.actions)

    def actions(self, action):
        command = action.text()
        if command == "Save all":
            self.save_all.emit()
        elif command == "Close all":
            self.close_all.emit()
        elif command == "Exit":
            self.exit.emit() 
        elif command == "Manual":
            QtWidgets.QMessageBox.information(self, "Manual", "Uputstvu za upotrebu programa Rukovalac informacionim resursima"
                + " mozete pristupiti klikom <a href='https://infhandler.zdelar.com'>ovde</a>")
        elif command == "About":
            QtWidgets.QMessageBox.information(self, "About", "Program Rukovalac informacionim resursima je realizovan" 
                + " u sklopu projekta iz predmeta Baze podataka i Specifikacija i modeliranje softvera. "
                + "Autor je Bojan Zdelar, ciji je broj indeksa 2019/270983")
