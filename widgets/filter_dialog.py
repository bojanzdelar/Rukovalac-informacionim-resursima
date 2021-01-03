from PySide2 import QtCore, QtWidgets, QtGui

class FilterDialog(QtWidgets.QDialog):
    changed = QtCore.Signal(list)

    def __init__(self, information_resource, attribute, text, parent=None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.attributes = information_resource.get_attribute()
        self.attribute = attribute
        self.text = text
        self.resize(300, 150)
        self.setWindowTitle("Edit filter")
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()

        label_attribute = QtWidgets.QLabel("Attribute", self)
        input_attribute = QtWidgets.QComboBox(self)
        input_attribute.addItems([attribute["display"] for attribute in self.attributes])
        input_attribute.setCurrentIndex(self.attribute)

        label_text = QtWidgets.QLabel("Text", self)
        input_text = QtWidgets.QLineEdit(self.text, self)

        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.action)

        layout.addWidget(label_attribute, 0, 0)
        layout.addWidget(input_attribute, 0, 1)
        layout.addWidget(label_text, 1, 0)
        layout.addWidget(input_text, 1, 1)
        layout.addWidget(button, 2, 1)

        return layout

    def action(self):
        attribute = self.layout().itemAtPosition(0, 1).widget().currentIndex()
        text = self.layout().itemAtPosition(1, 1).widget().text()
        self.changed.emit([attribute, text])
        self.close()