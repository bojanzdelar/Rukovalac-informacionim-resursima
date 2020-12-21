from meta.meta import read_meta
import csv
import operator

class InformationResource:
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta = read_meta()[file_name]
        self.data = self.read_data()

    def read_data(self):
        with open("data/" + self.file_name, "r", encoding="utf-8") as file:
            return [row for row in csv.reader(file)]

    def save_data(self):
        self.sort()
        with open("data/" + self.file_name, "w", encoding="utf-8", newline='') as file:
            csv.writer(file).writerows(self.data)

    def get_attribute(self, index=None):
        list = self.meta["attributes"]
        return list[index] if index is not None else list
    
    def get_attribute_index(self, attribute):
        if type(attribute) is dict:
            return self.get_attribute().index(attribute)
        for index, attr in enumerate(self.meta["attributes"]):
            if attribute == attr["name"]:
                return index

    def get_attributes_indexes(self, attributes):
        indexes = []
        if type(attributes) != list:
            attributes = [attributes]
        for attribute in attributes:
            indexes.append(self.get_attribute_index(attribute))
        return indexes

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

    def get_children(self):
        return self.meta["children"]

    def create_element(self, element):
        self.data.append(element)

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, element):
        self.data[index] = element

    def delete_element(self, index):
        self.data.pop(index)

    def column_values(self, column):
        values = set()
        index = self.get_attribute_index(column)
        for row in self.data:
            values.add(row[index])
        return sorted(values)

    def sort(self):
        primary_key = self.get_primary_key()
        if not len(primary_key):
            return False
        indexes = self.get_attributes_indexes(primary_key)
        self.data.sort(key = operator.itemgetter(*indexes))
        return True

    def filter(self, attributes, values):
        indexes = self.get_attributes_indexes(attributes)
        for element in reversed(self.data):
            for index, value in zip(indexes, values):
                if element[index] != value:
                    self.data.remove(element)
                    break

    def restrict(self, index, new_element=None):
        indexes = self.get_attributes_indexes(self.get_primary_key())
        children = self.get_children()
        for file_name, attributes in children.items():
            child = InformationResource(file_name)
            for i, attribute in zip(indexes, attributes):
                values = child.column_values(attribute)
                element = self.read_element(index)
                if element[i] in values and (not new_element or element[i] != new_element[i]):
                    return True
        return False