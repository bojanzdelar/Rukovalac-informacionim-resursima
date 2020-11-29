from PySide2 import QtWidgets

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.addMenu("File")
        self.addMenu("Edit")
        self.addMenu("View")
        self.addMenu("Help")