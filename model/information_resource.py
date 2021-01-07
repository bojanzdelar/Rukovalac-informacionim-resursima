from abc import ABC, abstractmethod
from meta.meta import read_meta

class InformationResource(ABC):
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta = read_meta()[file_name]
        self.data = self.read_data()

    @abstractmethod
    def read_data(self):
        ...

    @abstractmethod
    def save_data(self):
        ...

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

    @abstractmethod
    def filter(self, values):
        ...

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

    def get_parents(self):
        parents = {}
        for attribute in self.meta["attributes"]:
            if "relation" in attribute:
                parents.update(attribute["relation"])
        return parents