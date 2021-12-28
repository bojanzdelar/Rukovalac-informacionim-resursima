from PySide6 import QtCore, QtWidgets, QtGui
from .dialog import Dialog

class SplitDialog(Dialog):
    selected = QtCore.Signal(list)

    def __init__(self, information_resource, parent=None):
        super().__init__(parent) 

        self.attributes = information_resource.get_attribute()
        self.setWindowTitle("Split")
    
        label = QtWidgets.QLabel("Attribute: ", self)
        self.attribute = QtWidgets.QComboBox(self)
        self.attribute.currentIndexChanged.connect(self.change_input)
        self.attribute.addItems([attr["display"] for attr in self.attributes])
        button = QtWidgets.QPushButton("OK", self)
        button.clicked.connect(self.action)

        self.layout().addWidget(label, 0, 0)
        self.layout().addWidget(self.attribute, 0, 1)
        self.layout().addWidget(button, 2, 1)

    def change_input(self, index):
        attribute = self.attributes[index]
        operator = QtWidgets.QComboBox(self)
        operator.addItems(["=", "!="])
        if attribute["input"] in ["characters", "variable characters", "number"]:
            input = QtWidgets.QLineEdit(self)
            input.setMaxLength(attribute["length"])
            operator.addItems(["like", "not like"])
            if attribute["input"] == "characters":
                input.setValidator(QtGui.QRegularExpressionValidator(".{%s}" % attribute["length"]))
            elif attribute["input"] == "number":
                input.setValidator(QtGui.QRegularExpressionValidator("[1-9][0-9]*"))
                operator.addItems(["<", "<=", ">=", ">"])
        elif attribute["input"] == "date":
            input = QtWidgets.QDateEdit(self)
            input.setDisplayFormat("yyyy-MM-dd")
            input.setMinimumDate(QtCore.QDate.fromString("1900-01-01", "yyyy-MM-dd"))
            input.setMaximumDate(QtCore.QDate.currentDate().addYears(1))
            operator.addItems(["<", "<=", ">=", ">"])

        old_input = self.layout().itemAtPosition(1, 1)
        if old_input:
            self.layout().removeWidget(old_input.widget())
        old_operator = self.layout().itemAtPosition(1, 0)
        if old_operator:
            self.layout().removeWidget(old_operator.widget())

        self.layout().addWidget(input, 1, 1)
        self.layout().addWidget(operator, 1, 0)
    
    def action(self):
        attribute = self.attribute.currentIndex()
        operator = self.layout().itemAtPosition(1, 0).widget().currentText()
        input = self.layout().itemAtPosition(1, 1).widget().text()
        self.selected.emit([attribute, operator, input])
        self.accept()