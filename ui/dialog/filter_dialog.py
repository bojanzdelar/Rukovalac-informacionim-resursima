from PySide6 import QtCore, QtWidgets, QtGui
from .dialog import Dialog

class FilterDialog(Dialog):
    changed = QtCore.Signal(list)

    def __init__(self, information_resource, values, parent=None):
        super().__init__(parent) 

        self.attributes = information_resource.get_attribute()
        self.values = values
        self.setWindowTitle("Edit filter")

        for i, attribute in enumerate(self. attributes):
            label = QtWidgets.QLabel(attribute["display"], self)

            if attribute["input"] in ["characters", "variable characters", "number"]:
                input = QtWidgets.QLineEdit(self.values[i][1], self)
                input.setMaxLength(attribute["length"])
                char_width = QtGui.QFontMetrics(input.font()).averageCharWidth()
                input.setMaximumWidth(attribute["length"] * char_width + 10)
                if attribute["input"] == "number":
                    input.setValidator(QtGui.QRegularExpressionValidator("[0-9]*"))
            elif attribute["input"] == "date":
                input = QtWidgets.QDateEdit(QtCore.QDate.fromString(self.values[i][1], "yyyy-MM-dd"), self)
                input.setDisplayFormat("yyyy-MM-dd")
                input.setMinimumDate(QtCore.QDate.fromString("1900-01-01", "yyyy-MM-dd"))
                input.setMaximumDate(QtCore.QDate.currentDate().addYears(1))
                char_width = QtGui.QFontMetrics(input.font()).averageCharWidth()
                input.setMaximumWidth(10 * char_width + 10)

            operator = QtWidgets.QComboBox(self)
            operator.addItems(["=", "!="])
            if attribute["input"]  != "date":
                operator.addItems(["like", "not like"])
            if attribute["input"] in ["number", "date"]:
                operator.addItems(["<", "<=", ">=", ">"])
            operator.setCurrentText(self.values[i][0])

            self.layout().addWidget(label, i, 0)
            self.layout().addWidget(operator, i, 1)
            self.layout().addWidget(input, i, 2)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(self.action)
        self.layout().addWidget(self.button, i + 1, 2)
        
    def action(self):
        self.values = []
        for i in range(len(self.attributes)):
            operator = self.layout().itemAtPosition(i, 1).widget().currentText()
            input = self.layout().itemAtPosition(i, 2).widget().text()
            self.values.append((operator, input))
        self.changed.emit(self.values)
        self.close()