from PySide2 import QtCore, QtGui, QtWidgets
from abc import abstractmethod
from model.information_resource import InformationResource

class Dialog(QtWidgets.QDialog):
    def __init__(self, information_resource, parent = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)
        
        self.information_resource = information_resource
        self.attributes = self.information_resource.get_attribute()
        self.resize(300, len(self.attributes) * 35)
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()

        for i, attribute in enumerate(self.attributes):
            label = QtWidgets.QLabel(attribute["name"], self)
            if "foreign key" in attribute["type"]:
                input = QtWidgets.QComboBox(self)
                relation = [(k, v) for k,v in attribute["relation"].items()][0]
                values = InformationResource(relation[0]).column_values(relation[1])
                input.addItems(values)
            elif attribute["input"] in ["characters", "variable characters", "number"]:
                input = QtWidgets.QLineEdit(self)
                input.setMaxLength(attribute["length"])
                if attribute["input"] == "characters":
                    input.setValidator(QtGui.QRegExpValidator(".{%s}" % attribute["length"]))
                elif attribute["input"] == "number":
                    input.setValidator(QtGui.QRegExpValidator("[1-9][0-9]*"))
            elif attribute["input"] == "date":
                input = QtWidgets.QDateEdit(self)
                input.setMinimumDate(QtCore.QDate.fromString("01/01/1900", "dd/MM/yyyy"))
                input.setMaximumDate(QtCore.QDate.currentDate().addYears(1))
            layout.addWidget(label, i, 0)
            layout.addWidget(input, i, 1)
            
        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(self.action)
        layout.addWidget(self.button, i + 1, 1)

        return layout

    def validate_input(self):
        for i, attribute in enumerate(self.attributes):
            widget = self.layout().itemAtPosition(i, 1).widget()
            if "foreign key" in attribute["type"]:
                continue
            if "required" in attribute["type"] and widget.text() == "":
                label = self.layout().itemAtPosition(i, 0).widget().text()
                QtWidgets.QMessageBox.warning(self, "Greska", f"Polje {label} ne sme da bude prazno")
                return False
            if attribute["input"] != "date" and widget.validator():
                state = widget.validator().validate(widget.text(), 0)[0]
                if state != QtGui.QValidator.Acceptable:
                    label = self.layout().itemAtPosition(i, 0).widget().text()
                    QtWidgets.QMessageBox.warning(self, "Greska", f"Vrednost uneta u polje {label} nije dozvoljena")
                    return False
        return True

    @abstractmethod
    def action(self):
        ...