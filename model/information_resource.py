from abc import ABC, abstractmethod
from meta.meta import read_meta
import mysql.connector

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
    def filter(self, attributes, values):
        ...

    def get_attribute(self, index=None):
        list = self.meta["attributes"]
        return list[index] if index is not None else list