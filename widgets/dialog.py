from PySide2 import QtCore, QtWidgets
from abc import abstractmethod

class Dialog(QtWidgets.QDialog):
    def __init__(self, information_resource, parent = None):
        super().__init__(parent)

        self.information_resource = information_resource
        self.attributes = self.information_resource.get_attribute()
        self.resize(300, len(self.attributes) * 35)
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()
    
        for i, attribute in enumerate(self.attributes):
            label = QtWidgets.QLabel(attribute, self)
            input = QtWidgets.QLineEdit(self)
            layout.addWidget(label, i, 0)
            layout.addWidget(input, i, 1)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(self.action)
        layout.addWidget(self.button, i + 1, 1)

        return layout

    @abstractmethod
    def action(self):
        ...