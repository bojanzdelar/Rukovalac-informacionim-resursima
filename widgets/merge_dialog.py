from PySide2 import QtCore, QtWidgets, QtGui
from meta.meta import get_file_display, same_file_meta
from config.config import read_config
import os

class MergeDialog(QtWidgets.QDialog):
    selected = QtCore.Signal(list)

    def __init__(self, information_resource, parent = None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint) 

        self.information_resource = information_resource
        self.file_name = self.information_resource.file_name
        self.setWindowTitle("Merge")
        self.setWindowIcon(QtGui.QIcon("icons/app.png"))
        self.setLayout(QtWidgets.QGridLayout())
        self.generate_layout()

    def generate_layout(self):
        label = QtWidgets.QLabel("File: ", self)

        self.file = QtWidgets.QComboBox(self)
        file_organization = self.information_resource.get_type()
        self.files = os.listdir(read_config()[file_organization])
        self.files = [file for file in self.files \
            if same_file_meta(self.file_name, file, file_organization) and self.file_name != file]
        file_displays = [get_file_display(file, file_organization) for file in self.files]
        self.file.addItems(file_displays)

        button = QtWidgets.QPushButton("OK", self)
        button.clicked.connect(self.action)

        self.layout().addWidget(label, 0, 0)
        self.layout().addWidget(self.file, 0, 1)
        self.layout().addWidget(button, 1, 1)

    def action(self):
        current_index = self.file.currentIndex()
        self.selected.emit(self.files[current_index])
        self.close()