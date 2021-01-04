from PySide2 import QtCore, QtWidgets, QtGui

class FilterDialog(QtWidgets.QDialog):
    changed = QtCore.Signal(list)

    def __init__(self, information_resource, values, parent=None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint) 

        self.attributes = information_resource.get_attribute()
        self.values = values
        self.setWindowTitle("Edit filter")
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()

        for i, attribute in enumerate(self. attributes):
            label = QtWidgets.QLabel(attribute["display"], self)

            if attribute["input"] in ["characters", "variable characters", "number"]:
                input = QtWidgets.QLineEdit(self.values[i][1], self)
                input.setMaxLength(attribute["length"])
                if attribute["input"] == "number":
                    input.setValidator(QtGui.QRegExpValidator("[0-9]*"))
            elif attribute["input"] == "date":
                input = QtWidgets.QDateEdit(QtCore.QDate.fromString(self.values[i][1], "dd/MM/yyyy"), self)
                input.setDisplayFormat("dd/MM/yyyy")
                input.setMinimumDate(QtCore.QDate.fromString("01/01/1900", "dd/MM/yyyy"))
                input.setMaximumDate(QtCore.QDate.currentDate().addYears(1))

            operator = QtWidgets.QComboBox(self)
            operator.addItems(["=", "!="])
            if attribute["input"]  != "date":
                operator.addItems(["like", "not like"])
            if attribute["input"] in ["number", "date"]:
                operator.addItems(["<", "<=", ">=", ">"])
            operator.setCurrentText(self.values[i][0])

            layout.addWidget(label, i, 0)
            layout.addWidget(operator, i, 1)
            layout.addWidget(input, i, 2)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(self.action)
        layout.addWidget(self.button, i + 1, 2)

        return layout
        
    def action(self):
        self.values = []
        for i in range(len(self.attributes)):
            operator = self.layout().itemAtPosition(i, 1).widget().currentText()
            input = self.layout().itemAtPosition(i, 2).widget().text()
            self.values.append((operator, input))
        self.changed.emit(self.values)
        self.close()