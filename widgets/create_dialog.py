from PySide2 import QtCore
from model.serial_file import SerialFile
from widgets.dialog import Dialog

class CreateDialog(Dialog):
    def __init__(self, information_resource, parent = None):
        super().__init__(information_resource, parent)

        self.setWindowTitle("Create")

    def action(self):
        if not self.validate_input():
            return
        element = []
        for index, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(index, 1).widget()
            text = widget.currentText() if "foreign key" in attribute["type"] else widget.text()
            element.append(text)
        if self.information_resource.create_element(element):
            self.close()