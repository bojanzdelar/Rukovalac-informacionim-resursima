from PySide2 import QtCore, QtWidgets
from widgets.dialog import Dialog

class CreateDialog(Dialog):
    def __init__(self, information_resource, parent = None):
        super().__init__(information_resource, parent)

        self.setWindowTitle("Create")

    def action(self):
        if not self.validate():
            return
        element = []
        for index in range(len(self.attributes)):
            element.append(self.layout().itemAtPosition(index, 1).widget().text())
        self.information_resource.create_element(element)
        self.close()