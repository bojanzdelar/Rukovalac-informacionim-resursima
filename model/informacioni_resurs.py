from abc import ABC

import csv
import json

class InformacioniResurs(ABC):
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

    def get_subtables(self):
        return self.meta["subtables"]

    def get_attribute(self, index):
        return self.get_attributes()[index]

    def get_attributes(self):
        return self.meta["attributes"]