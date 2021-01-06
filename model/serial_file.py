from model.information_resource import InformationResource
from config.config import read_config
from datetime import datetime
import csv
import operator 

ops = {
    "=" : operator.eq,
    "!=" : operator.ne,
    "<" : operator.lt,
    "<=" : operator.le,
    ">=" : operator.ge,
    ">" : operator.gt,
    "like" : operator.contains,
}

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

    def filter(self, values):
        hide_indexes = []
        for index in range(len(self.data)):
            element = self.read_element(index).copy()
            match_filter = True
            for i in range(len(element)):
                operator, text = values[i]
                input_type = self.get_attribute(i)["input"]
                if (text == "") or (input_type == "date" and text == "01/01/1900"):
                    continue
                if input_type == "date":
                    text = datetime.strptime(text, "%d/%m/%Y")
                    element[i] = datetime.strptime(str(element[i]), "%d/%m/%Y")
                elif input_type != "number":
                    text = text.lower()
                    element[i] = element[i].lower()
                if (operator == "not like" and ops["like"](element[i], text)) \
                        or (operator != "not like" and not ops[operator](element[i], text)):
                    match_filter = False
                    break
            if not match_filter:
                hide_indexes.append(index)
        return hide_indexes
    
    def column_values(self, column):
        values = set()
        index = self.get_attribute_index(column)
        for row in self.data:
            values.add(row[index])
        return sorted(values)
