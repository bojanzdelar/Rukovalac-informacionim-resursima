from PySide2 import QtCore, QtWidgets
from widgets.dialog import Dialog
from model.information_resource import InformationResource

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
            if "foreign key" in attribute["type"]:
                widget.setCurrentIndex(widget.findText(element[i]))
            elif attribute["input"] == "date":
                widget.setDate(QtCore.QDate.fromString(element[i], "dd/MM/yyyy"))
            else:   
                widget.setText(element[i])

    def restrict(self, new_element):
        indexes = self.information_resource.get_attributes_indexes(self.information_resource.get_primary_key())
        children = self.information_resource.get_children()
        for file_name, attributes in children.items():
            child = InformationResource(file_name)
            for i, attribute in zip(indexes, attributes):
                values = child.column_values(attribute)
                element = self.information_resource.read_element(self.index)
                if element[i] in values and element[i] != new_element[i]:
                    return True
        return False

    def action(self):
        if not self.validate_input():
            return
        element = []
        for i, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(i, 1).widget()
            text = widget.currentText() if "foreign key" in attribute["type"] else widget.text()
            element.append(text)
        primary_key_used, position = self.information_resource.primary_key_used(element)
        if primary_key_used and self.index != position: 
            QtWidgets.QMessageBox.about(self, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return
        if self.restrict(element):
            QtWidgets.QMessageBox.about(self, "Greska", "Ne mozete da izmenite vrednost primarnog kljuca" 
                + " koji se koristi kao strani kljuc u child tabelama")
            return
        self.information_resource.update_element(self.index, element)
        self.close()