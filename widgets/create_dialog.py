from PySide2 import QtCore, QtWidgets
from widgets.dialog import Dialog

class CreateDialog(Dialog):
    def __init__(self, information_resource, parent = None):
        super().__init__(information_resource, parent)

        self.setWindowTitle("Create")

    def action(self):
        if not self.validate_input():
            return
        element = []
        for index in range(len(self.attributes)):
            element.append(self.layout().itemAtPosition(index, 1).widget().text())
        primary_key_used, _ = self.information_resource.primary_key_used(element)
        if primary_key_used:
            QtWidgets.QMessageBox.about(self, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return
        self.information_resource.create_element(element)
        self.close()