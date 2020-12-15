import csv
import json

class InformationResource:
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta = self.read_meta()
        self.data = self.read_data()

    def read_meta(self):
        with open("meta.json", "r", encoding="utf-8") as file:
            return json.load(file)[self.file_name]
    
    def read_data(self):
        with open("data/" + self.file_name, "r", encoding="utf-8") as file:
            return [row for row in csv.reader(file)]

    def save_data(self):
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
            if attribute["type"] == "primary key":
                primary_key.append(attribute)
        return primary_key

    def get_relations(self):
        return self.meta["relations"]

    def get_children(self):
        children = {}
        relations = self.get_relations()
        for key, value in relations.items():
            if value["type"] == "child":
                children[key] = value
        return children

    def create_element(self, element):
        self.data.append(element)

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, element):
        self.data[index] = element

    def delete_element(self, index):
        self.data.pop(index)

    def filter(self, attributes, values):
        indexes = self.get_attributes_indexes(attributes)
        for element in reversed(self.data):
            for index, value in zip(indexes, values):
                if element[index] != value:
                    self.data.remove(element)
                    break