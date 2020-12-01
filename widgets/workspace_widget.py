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
        self.ustanova_model = self.create_dummy_model() # FIXME: privremeno
        self.main_table.setModel(self.ustanova_model) # FIXME: privremeno
        self.main_table.clicked.connect(self.ustanova_selected) # FIXME: privremeno
        
        self.tab_widget = None
        self.create_tab_widget()
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def ustanova_selected(self, index):
        selected_ustanova = self.main_table.model().get_element(index)
        self.tab_widget.clear()

        studenti = QtWidgets.QTableView(self.tab_widget)
        student_model = StudentModel()
        student_model.students = selected_ustanova.studenti
        studenti.setModel(student_model)

        self.tab_widget.addTab(studenti, "Studenti")

    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)
        self.show_tabs()
        
    def show_tabs(self):
        self.tab_widget.addTab(QtWidgets.QTableWidget(), "Podtabela 1") # FIXME: privremeno
        self.tab_widget.addTab(QtWidgets.QTableWidget(), "Podtabela 2") # FIXME: privremeno
        
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def create_dummy_model(self):
        ustanove_model = VisokoskolskaUstanovaModel()
        ustanove_model.ustanove = [
            VisokoskolskaUstanova("TF", "Tehnicki fakultet", "Novi Sad", [
                Student("TF", "2019270983", "Zdelar", "Bojan"),
                Student("TF", "2019270366", "Markovic", "Marko")
            ]),
            VisokoskolskaUstanova("FIR", "Fakultet za informatiku i racunarstvo", "Beograd", [
                Student("FIR", "2018270643", "Peric", "Petar")
            ])
        ]
        return ustanove_model