from PySide6 import QtCore
from dialog.dialog import Dialog
from model.sequential_file import SequentialFile
from model.database import Database

class CreateDialog(Dialog):
    created = QtCore.Signal()

    def __init__(self, information_resource, parent = None):
        super().__init__(information_resource, parent)

        self.setWindowTitle("Create")

    def action(self):
        if not self.validate_input():
            return
        element = []
        for index, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(index, 1).widget()
            if "foreign key" in attribute["type"] and isinstance(self.information_resource, (SequentialFile, Database)):
                text = widget.currentText()
            else:
                text = widget.text()
            element.append(text)
        if self.information_resource.create_element(element):
            self.created.emit()