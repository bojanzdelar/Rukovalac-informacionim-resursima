from PySide2 import QtWidgets, QtGui
from model.visokoskolska_ustanova_model import VisokoskolskaUstanovaModel # TODO: obrisi me 
from model.visokoskolska_ustanova import VisokoskolskaUstanova
from model.student_model import StudentModel
from model.student import Student

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, file_name, parent):
        super().__init__(parent)

        self.file_name = file_name
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_table = self.create_main_table()
        self.tab_widget = self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return table

    def create_main_table(self):
        if self.file_name == "visokoskolske_ustanove.csv":
            model = VisokoskolskaUstanovaModel()
            model.ustanove = VisokoskolskaUstanova.load()       
        elif self.file_name == "student.csv":
            model = StudentModel()
            model.students = Student.load()      
        
        main_table = self.create_table()
        main_table.setModel(model)
        main_table.clicked.connect(self.selected)
        return main_table

    def selected(self, index):
        if self.file_name == "visokoskolske_ustanove.csv":
            selected_ustanova = self.main_table.model().get_element(index)
            student_model = StudentModel()
            student_model.students = selected_ustanova.studenti
            studenti = self.create_table(self.tab_widget)
            studenti.setModel(student_model)

            self.tab_widget.clear()
            self.tab_widget.addTab(studenti, "Studenti")

        # elif self.file_name == "student.csv":
        #     ...

    def create_tab_widget(self):
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.delete_tab)
        return tab_widget
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)