from PySide2 import QtWidgets
from model.information_resource import InformationResource
from config.config import read_config
import mysql.connector
from decimal import Decimal

class Database(InformationResource):
    def __init__(self, file_name):
        self.connect()

        super().__init__(file_name)

    def __del__(self):
        self.disconnect()

    def connect(self):
        config = read_config()
        self.connection = mysql.connector.connect(user=config["user"], password=config["password"], 
                                                  host=config["host"], database=config["database"])
        self.csor = self.connection.cursor()

    def disconnect(self):
        self.csor.close()
        self.connection.close()

    def read_data(self):
        self.csor.callproc("show_table", [self.file_name[0:-4]])
        for res in self.csor.stored_results():
            return res.fetchall()

    def save_data(self):
        self.connection.commit()
        self.data = self.read_data()

    def create_element(self, element):
        arguments = "(" + ", ".join([f"'{attribute}'" for attribute in element]) + ")"
        try:
            self.csor.callproc("insert_element", [self.file_name[0:-4], arguments])
            return super().create_element(element)
        except mysql.connector.errors.IntegrityError:
            QtWidgets.QMessageBox.warning(None, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return False

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, element):
        ...

    def delete_element(self, index):
        element = self.data[index]
        arguments = ""
        for i, el in enumerate(element): 
            name = self.meta["attributes"][i]["name"]
            arguments += f"({name} = '{element[i]}')"
            if i != len(element) - 1:
                arguments += " AND "
        try:
            self.csor.callproc("delete_element", [self.file_name[0:-4], arguments])
            super().delete_element(index)
        except mysql.connector.errors.IntegrityError:
            QtWidgets.QMessageBox.warning(None, "Greska", "Ne mozete da obrisete entitet" 
                + " cije se vrednosti primarnog kljuca koriste kao strani kljuc u child tabelama")

    def filter(self, attributes, values):
        ...

    def column_values(self, column):
        self.csor.callproc("column_values", [column, self.file_name[0:-4]])
        for res in self.csor.stored_results():
            values = res.fetchall()
        return sorted([str(value[0]) for value in values])