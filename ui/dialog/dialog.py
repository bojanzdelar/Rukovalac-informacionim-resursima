from PySide6 import QtCore, QtGui, QtWidgets
from abc import abstractmethod

class Dialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.setWindowIcon(QtGui.QIcon("icons/app.png"))
        self.setLayout(QtWidgets.QGridLayout())        

    @abstractmethod
    def action(self):
        ...