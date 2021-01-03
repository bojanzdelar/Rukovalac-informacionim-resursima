from PySide2 import QtCore
from widgets.dialog import Dialog
from model.sequential_file import SequentialFile

class UpdateDialog(Dialog):
    def __init__(self, information_resource, index, parent = None):
        super().__init__(information_resource, parent)

        self.index = index
        self.fill_input()
        self.setWindowTitle("Update")

    def fill_input(self):
        element = self.information_resource.read_element(self.index)
        for i, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(i, 1).widget()
            if "foreign key" in attribute["type"] and isinstance(self.information_resource, SequentialFile):
                widget.setCurrentIndex(widget.findText(element[i]))
            elif attribute["input"] == "date":
                widget.setDate(QtCore.QDate.fromString(element[i], "dd/MM/yyyy"))
            else:   
                widget.setText(element[i])

    def action(self):
        if not self.validate_input():
            return
        element = []
        for i, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(i, 1).widget()
            if "foreign key" in attribute["type"] and isinstance(self.information_resource, SequentialFile):
                text = widget.currentText()
            else:
                text = widget.text()
            element.append(text)
        if self.information_resource.update_element(self.index, element):
            self.close()