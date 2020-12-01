from PySide2 import QtWidgets, QtGui
from model.visokoskolska_ustanova_model import VisokoskolskaUstanovaModel # TODO: obrisi me 
from model.visokoskolska_ustanova import VisokoskolskaUstanova
from model.student_model import StudentModel
from model.student import Student

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_table = QtWidgets.QTableView()
        self.main_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # FIXME: privremeno
        self.ustanova_model = VisokoskolskaUstanovaModel()
        self.ustanova_model.ustanove = VisokoskolskaUstanova.load()
        self.main_table.setModel(self.ustanova_model)
        self.main_table.clicked.connect(self.ustanova_selected)
        
        self.tab_widget = None
        self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def ustanova_selected(self, index):
        student_model = StudentModel()
        selected_ustanova = self.main_table.model().get_element(index)
        student_model.students = selected_ustanova.studenti
        studenti = QtWidgets.QTableView(self.tab_widget)
        studenti.setModel(student_model)

        self.tab_widget.clear()
        self.tab_widget.addTab(studenti, "Studenti")

    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)