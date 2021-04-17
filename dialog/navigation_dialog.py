from PySide6 import QtCore, QtWidgets

class NavigationDialog(QtWidgets.QDialog):
    selected = QtCore.Signal(str)

    def __init__(self, tables, parent=None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        self.tables = tables
        self.setWindowTitle("Izbor tabele")
        self.setLayout(self.generate_layout())

    def generate_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Tabela", self), 0, 0)
        self.combo_box = QtWidgets.QComboBox(self)
        for table in self.tables:
            self.combo_box.addItem(table)
        layout.addWidget(self.combo_box, 0, 1)
        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.action)
        layout.addWidget(button, 1, 1)
        return layout

    def action(self):
        selected_table = self.combo_box.currentText()
        self.selected.emit(self.tables[selected_table])
        self.close()