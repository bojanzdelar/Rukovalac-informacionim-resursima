from abc import ABC, abstractmethod
from meta.meta import get_file_meta

class InformationResource(ABC):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_type, self.meta = self.read_meta()
        self.data = self.read_data()

    @abstractmethod 
    def get_type(self):
        ...

    def read_meta(self):
        return get_file_meta(self.file_name, self.get_type())

    @abstractmethod
    def read_data(self):
        ...

    @abstractmethod
    def save_data(self):
        ...

    @abstractmethod
    def create_element(self, element):
        ...

    @abstractmethod
    def read_element(self, index):
        ...

    @abstractmethod
    def update_element(self, index, element):
        ...

    @abstractmethod
    def delete_element(self, index):
        ...
        
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