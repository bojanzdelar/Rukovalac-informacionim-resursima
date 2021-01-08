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

    def create_element(self, element):
        values = "(" + ", ".join([f"'{attribute}'" for attribute in element]) + ")"
        try:
            self.csor.callproc("insert_element", [self.file_name[0:-4], values])
            return super().create_element(element)
        except mysql.connector.errors.IntegrityError:
            QtWidgets.QMessageBox.warning(None, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return False

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, new_element):
        element = self.data[index]
        set = []
        where = []
        primary_key_indexes = self.get_attributes_indexes(self.get_primary_key())
        for i, el in enumerate(new_element):
            if element[i] != el:
                name = self.meta["attributes"][i]["name"]
                set.append(f"{name} = '{new_element[i]}'")
            if i in primary_key_indexes:
                name = self.meta["attributes"][i]["name"]
                where.append(f"{name} = '{element[i]}'")
        set = ", ".join(set)
        where = " AND ".join(where)
        try:
            self.csor.callproc("update_element", [self.file_name[0:-4], set, where])
            return super().update_element(index, new_element)
        except mysql.connector.errors.IntegrityError as error:
            QtWidgets.QMessageBox.warning(None, "Greska", 
                "Vrednost uneta u polje primarnog kljuca je zauzeta" if error.errno == 1062
                else "Ne mozete da izmenite vrednost primarnog kljuca koji se koristi kao strani kljuc u child tabelama")
            return False

    def delete_element(self, index):
        element = self.data[index]
        where = []
        for i, el in enumerate(element): 
            name = self.meta["attributes"][i]["name"]
            where.append(f"({name} = '{element[i]}')")
        where = " AND ".join(where)
        try:
            self.csor.callproc("delete_element", [self.file_name[0:-4], where])
            super().delete_element(index)
        except mysql.connector.errors.IntegrityError:
            QtWidgets.QMessageBox.warning(None, "Greska", "Ne mozete da obrisete entitet" 
                + " cije se vrednosti primarnog kljuca koriste kao strani kljuc u child tabelama")

    def filter(self, values):
        where = []
        for i in range(len(values)):
            attribute = self.get_attribute(i)
            name = attribute["name"]
            operator = values[i][0]
            value = values[i][1]
            if (value == "") or (attribute["input"] == "date" and value == "1900-01-01"):
                continue
            if "like" in operator:
                value = f"%{value}%"
            where.append(f"{name} {operator} '{value}'")
        if not len(where):
            return
        where = " AND ".join(where)
        self.csor.callproc("select_where", [self.file_name[0:-4], where])
        for res in self.csor.stored_results():
            self.data = res.fetchall()

    def get_children(self, index):
        children_meta = self.meta["children"]
        children = []
        for file_name, attributes in children_meta.items():
            main_attributes = self.get_primary_key()
            main_attributes_indexes = self.get_attributes_indexes(main_attributes)
            values = []
            for attr_index in main_attributes_indexes:
                values.append(self.read_element(index)[attr_index])

            child = Database(file_name)
            
            where = []
            for attribute, value in zip(attributes, values):
                where.append(f"{attribute} = '{value}'")
            where = " AND ".join(where)

            self.csor.callproc("select_where", [file_name[0:-4], where])
            for res in self.csor.stored_results():
                child.data = res.fetchall()

            children.append(child)

        return children

    def get_primary_key(self):
        primary_key = []
        for attribute in self.meta["attributes"]:
            if "primary key" in attribute["type"]:
                primary_key.append(attribute)
        return primary_key

    def column_values(self, column):
        self.csor.callproc("column_values", [column, self.file_name[0:-4]])
        for res in self.csor.stored_results():
            values = res.fetchall()
        return sorted([str(value[0]) for value in values])