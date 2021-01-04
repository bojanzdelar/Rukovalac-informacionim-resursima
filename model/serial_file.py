from model.information_resource import InformationResource
from config.config import read_config
import csv

class SerialFile(InformationResource):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read_data(self):
        path = read_config()["serial_data"]
        with open(path + self.file_name, "r", encoding="utf-8") as file:
            return [row for row in csv.reader(file)]

    def save_data(self):
        path = read_config()["serial_data"]
        with open(path + self.file_name, "w", encoding="utf-8", newline='') as file:
            csv.writer(file).writerows(self.data)

    def create_element(self, element):
        self.data.append(element)
        return True

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, element):
        self.data[index] = element
        return True

    def delete_element(self, index):
        self.data.pop(index)

    def filter(self, attributes, values):
        indexes = self.get_attributes_indexes(attributes)
        for element in reversed(self.data):
            for index, value in zip(indexes, values):
                if element[index] != value:
                    self.data.remove(element)
                    break
    
    def column_values(self, column):
        values = set()
        index = self.get_attribute_index(column)
        for row in self.data:
            values.add(row[index])
        return sorted(values)
