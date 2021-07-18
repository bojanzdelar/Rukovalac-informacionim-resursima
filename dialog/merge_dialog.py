from PySide6 import QtCore, QtWidgets
from dialog.dialog import Dialog
from meta.meta import get_display

class MergeDialog(Dialog):
    selected = QtCore.Signal(str)
    merged = QtCore.Signal(str, str)

    def __init__(self, information_resource, files, parent = None):
        super().__init__(parent) 

        self.information_resource = information_resource
        self.files = files
        self.file_name = self.information_resource.name
        self.file_organization = self.information_resource.type
        
        self.setWindowTitle("Merge")
        
        label = QtWidgets.QLabel("File: ", self)

        self.file = QtWidgets.QComboBox(self)
        
        file_displays = [get_display(file, self.file_organization) for file in self.files]
        self.file.addItems(file_displays)

        button = QtWidgets.QPushButton("OK", self)
        button.clicked.connect(self.action)

        self.layout().addWidget(label, 0, 0)
        self.layout().addWidget(self.file, 0, 1)
        self.layout().addWidget(button, 1, 1)

    def action(self):
        current_index = self.file.currentIndex()
        other_file_name = self.files[current_index]
        self.selected.emit(other_file_name)
        self.merged.emit(other_file_name, "merge")
        self.accept()