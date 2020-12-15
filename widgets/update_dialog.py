from PySide2 import QtCore, QtWidgets
from widgets.dialog import Dialog

class UpdateDialog(Dialog):
    def __init__(self, information_resource, index, parent = None):
        super().__init__(information_resource, parent)

        self.index = index
        self.fill_input()
        self.setWindowTitle("Update")

    def fill_input(self):
        element = self.information_resource.read_element(self.index)
        for index, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(index, 1).widget()
            if attribute["input"] == "date":
                widget.setDate(QtCore.QDate.fromString(element[index], "dd/MM/yyyy"))
            else:   
                widget.setText(element[index])

    def action(self):
        if not self.validate():
            return
        element = []
        for index in range(len(self.attributes)):
            element.append(self.layout().itemAtPosition(index, 1).widget().text())
        self.information_resource.update_element(self.index, element)
        self.close()