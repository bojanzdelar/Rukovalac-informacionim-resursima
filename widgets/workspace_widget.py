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
        self.main_table = None
        self.create_main_table()
        self.tab_widget = None
        self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def create_table(self, parent = None):
        table = QtWidgets.QTableView(parent)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return table

    def create_main_table(self):
        self.main_table = self.create_table()

        if self.file_name == "visokoskolske_ustanove.csv":
            self.model = VisokoskolskaUstanovaModel()
            self.model.ustanove = VisokoskolskaUstanova.load()
            self.main_table.setModel(self.model)
            self.main_table.clicked.connect(self.selected)
            
        elif self.file_name == "student.csv":
            self.model = StudentModel()
            self.model.students = Student.load()      
            self.main_table.setModel(self.model)
            self.main_table.clicked.connect(self.selected)

    def selected(self, index):
        if self.file_name == "visokoskolske_ustanove.csv":
            student_model = StudentModel()
            selected_ustanova = self.main_table.model().get_element(index)
            student_model.students = selected_ustanova.studenti
            studenti = self.create_table(self.tab_widget)
            studenti.setModel(student_model)

            self.tab_widget.clear()
            self.tab_widget.addTab(studenti, "Studenti")

        # elif self.file_name == "student.csv":
        #     ...

    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)