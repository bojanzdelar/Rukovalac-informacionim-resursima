from model.information_resource import InformationResource
from config.config import read_config
import mysql.connector

class Database(InformationResource):
    def __init__(self, file_name):
        self.connect()

        super().__init__(file_name)

    def __del__(self):
        self.disconnect()

    def connect(self):
        config = read_config()
        self.connection = mysql.connector.connect(user=config["user"], password=config["password"], 
                                                  host=config["host"], database=config["database"])
        self.csor = self.connection.cursor()

    def disconnect(self):
        self.csor.close()
        self.connection.close()

    def read_data(self):
        self.csor.callproc("show_table", [self.file_name[0:-4]])
        for res in self.csor.stored_results():
            return res.fetchall()

    def save_data(self):
        self.connection.commit()
        print("test")

    def create_element(self, element):
        ...

    def read_element(self, index):
        return self.data[index]

    def update_element(self, index, element):
        ...

    def delete_element(self, index):
        ...

    def filter(self, attributes, values):
        ...

    def column_values(self, column):
        self.csor.callproc("column_values", [column, self.file_name[0:-4]])
        for res in self.csor.stored_results():
            values = res.fetchall()
        return sorted([str(value[0]) for value in values])