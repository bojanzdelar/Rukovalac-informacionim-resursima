from PySide2 import QtCore, QtWidgets

class CreateDialog(QtWidgets.QDialog):
    created = QtCore.Signal(list)

    def __init__(self, information_resource, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Create")
        self.information_resource = information_resource
        self.attributes = self.information_resource.get_attribute()
        self.resize(300, len(self.attributes) * 35)
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()
    
        for index, attribute in enumerate(self.attributes):
            label = QtWidgets.QLabel(attribute, self)
            input = QtWidgets.QLineEdit(self)
            layout.addWidget(label, index, 0)
            layout.addWidget(input, index, 1)

        self.button = QtWidgets.QPushButton("Create", self)
        self.button.clicked.connect(self.create)
        layout.addWidget(self.button, index + 1, 1)

        return layout

    def create(self):
        element = []
        for index in range(len(self.attributes)):
            element.append(self.layout().itemAtPosition(index, 1).widget().text())
        self.information_resource.data.append(element)
        self.close()
