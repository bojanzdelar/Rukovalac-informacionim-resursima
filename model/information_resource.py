import csv
import json

class InformationResource:
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta = self.read_meta(file_name)
        self.data = self.read_data(file_name)

    def read_meta(self, file_name):
        with open("meta.json") as file:
            return json.load(file)[self.file_name]
    
    def read_data(self, file_name):
        with open("data/" + file_name) as file:
            return [row for row in csv.reader(file)]

    def get_attribute(self, index=None):
        list = self.meta["primary key"] + self.meta["foreign key"] + self.meta["attributes"]
        return list[index] if index else list
    
    def get_attribute_index(self, attribute):
        return self.get_attribute().index(attribute)

    def get_attributes_indexes(self, attributes):
        indexes = []
        for attribute in attributes:
            indexes.append(self.get_attribute_index(attribute))
        return indexes

    def get_relations(self):
        return self.meta["relations"]

    def filter(self, attributes, values):
        indexes = self.get_attributes_indexes(attributes)
        for element in reversed(self.data):
            for index, value in zip(indexes, values):
                if element[index] != value:
                    self.data.remove(element)
                    break