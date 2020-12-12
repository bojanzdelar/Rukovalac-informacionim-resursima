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
            return [row for row in csv.reader(file, delimiter=";")]

    def get_attributes(self):
        return self.meta["primary key"] + self.meta["attributes"]

    def get_attribute(self, index):
        return self.get_attributes()[index]
    
    def get_attribute_index(self, attribute):
        return self.get_attributes().index(attribute)

    def get_relations(self):
        return self.meta["relations"]

    def filter(self, attribute, value):
        index = self.get_attribute_index(attribute)
        for element in reversed(self.data):
            if element[index] != value:
                self.data.remove(element)