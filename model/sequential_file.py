from PySide2 import QtWidgets
from model.serial_file import SerialFile
from model.external_merge_sort import ExternalMergeSort
from meta.meta import get_files
from config.config import read_config
import csv
import os.path
import operator

class SequentialFile(SerialFile):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_type(self):
        return "sequential"
        
    def read_multiple_data(self, files):
        path = read_config()[self.get_type()]
        data = []
        for file_name in files:
            if not os.path.exists(path + file_name):
                continue
            with open(path + file_name, "r", encoding="utf-8") as file:
                data += [row for row in csv.reader(file)]
        return data

    def create_element(self, element):
        primary_key_used, _ = self.primary_key_used(element)
        if primary_key_used:
            QtWidgets.QMessageBox.warning(None, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return False
        return super().create_element(element)

    def update_element(self, index, element):
        primary_key_used, position = self.primary_key_used(element)
        if primary_key_used and index != position: 
            QtWidgets.QMessageBox.warning(None, "Greska", "Vrednost uneta u polje primarnog kljuca je zauzeta")
            return False
        if self.restrict_update(index, element):
            QtWidgets.QMessageBox.warning(None, "Greska", "Ne mozete da izmenite vrednost primarnog kljuca" 
                + " koji se koristi kao strani kljuc u child tabelama")
            return False
        return super().update_element(index, element)

    def delete_element(self, index):
        if self.restrict_remove(index):
            QtWidgets.QMessageBox.warning(None, "Greska", "Ne mozete da obrisete entitet" 
                + " cije se vrednosti primarnog kljuca koriste kao strani kljuc u child tabelama")
            return
        super().delete_element(index)

    def get_children(self, index):
        children_meta = self.meta["children"]
        children = []
        path = read_config()[self.get_type()]

        for file_type, attributes in children_meta.items():
            main_attributes = self.get_primary_key()
            main_attributes_indexes = self.get_attributes_indexes(main_attributes)
            values = []
            for attr_index in main_attributes_indexes:
                values.append(self.read_element(index)[attr_index])

            file_names = get_files(file_type, self.get_type())
            child = SequentialFile(list(file_names.keys())[0])
            child.data = child.read_multiple_data(file_names.keys())
            child._sort_child()
            child._filter_child(attributes, values)
            children.append(child)

        return children

    def _filter_child(self, attributes, values):
        indexes = self.get_attributes_indexes(attributes)
        for element in reversed(self.data):
            for index, value in zip(indexes, values):
                if element[index] != value:
                    self.data.remove(element)
                    break

    def _sort_child(self):
        indexes = self.get_attributes_indexes(self.get_primary_key())
        self.data.sort(key = operator.itemgetter(*indexes))

    def get_primary_key(self):
        primary_key = []
        for attribute in self.meta["attributes"]:
            if "primary key" in attribute["type"]:
                primary_key.append(attribute)
        return primary_key

    def primary_key_used(self, new_element):
        indexes = self.get_attributes_indexes(self.get_primary_key())
        if not len(indexes):
            return False, -1
        for i, element in enumerate(self.data):
            unique = False
            for index in indexes:
                if new_element[index] != element[index]:
                    unique = True
                    break
            if not unique:
                return True, i
        return False, -1
    
    def restrict_update(self, index, new_element):
        indexes = self.get_attributes_indexes(self.get_primary_key())
        children = self.meta["children"]
        for file_name, attributes in children.items():
            child = SequentialFile(file_name)
            for i, attribute in zip(indexes, attributes):
                values = child.column_values(attribute)
                element = self.read_element(index)
                if element[i] in values and element[i] != new_element[i]:
                    return True
        return False

    def restrict_remove(self, index):
        indexes = self.get_attributes_indexes(self.get_primary_key())
        children = self.meta["children"]
        for file_name, attributes in children.items():
            child = SequentialFile(file_name)
            used = True
            for i, attribute in zip(indexes, attributes):
                values = child.column_values(attribute)
                element = self.read_element(index)
                if not element[i] in values:
                    used = False
                    break
            if used:
                return True
        return False