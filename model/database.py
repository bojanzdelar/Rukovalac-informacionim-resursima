from model.information_resource import InformationResource
import mysql.connector

class Database(InformationResource):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read_data(self):
        connection = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="univerzitet")
        csor = connection.cursor()
        
        csor.callproc("show_table", [self.file_name[0:-4]])
        for res in csor.stored_results():
            data = res.fetchall()

        csor.close()
        connection.close()

        return data

    def read_element(self, index):
        return self.data[index]