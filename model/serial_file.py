from PySide2 import QtCore
from model.information_resource import InformationResource
from meta.meta import get_file_display, file_in_meta, add_file, remove_file
from config.config import read_config
from datetime import datetime
import csv
import operator
import os.path 

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
   
    def get_type(self):
        return "serial"

    def read_data(self):
        path = read_config()[self.get_type()]
        if not os.path.exists(path + self.file_name):
            return []
        with open(path + self.file_name, "r", encoding="utf-8") as file:
            return [row for row in csv.reader(file)]

    def save_data(self):
        path = read_config()[self.get_type()]
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
        show_indexes = []
        for index in range(len(self.data)):
            element = self.read_element(index).copy()
            match_filter = True
            for i in range(len(element)):
                operator, text = values[i]
                input_type = self.get_attribute(i)["input"]
                if (text == "") or (input_type == "date" and text == "1900-01-01"):
                    continue
                if input_type == "date":
                    text = datetime.strptime(text, "%Y-%m-%d")
                    element[i] = datetime.strptime(str(element[i]), "%Y-%m-%d")
                elif input_type != "number":
                    text = text.lower()
                    element[i] = element[i].lower()
                if (operator == "not like" and ops["like"](element[i], text)) \
                        or (operator != "not like" and not ops[operator](element[i], text)):
                    match_filter = False
                    break
            if match_filter:
                show_indexes.append(index)
        return show_indexes

    def split(self, condition):
        i, operator, text = condition
        path = read_config()[self.get_type()]
        file_name = self.file_name
        file_name_1 = (file_name[0:-4] + "--"  
            + self.get_attribute(i)["name"] + operator + text + ".csv")
        file_name_2 = (file_name[0:-4] + "--not(" 
            + self.get_attribute(i)["name"] + operator + text + ").csv")
        file_display_1 = (get_file_display(file_name, self.get_type()) + " -- "
            + self.get_attribute(i)["display"] + " " + operator + " " + text)
        file_display_2 = (get_file_display(file_name, self.get_type()) + " -- not ("
            + self.get_attribute(i)["display"] + " " + operator + " " + text + ")")

        new_file = open(path + file_name_1, "w")
        new_file.close()

        new_file = open(path + file_name_2, "w")
        new_file.close()

        for index in range(len(self.data)):
            element = self.read_element(index).copy()
            
            input_type = self.get_attribute(i)["input"]
            if input_type == "date":
                text = datetime.strptime(text, "%Y-%m-%d")
                element[i] = datetime.strptime(str(element[i]), "%Y-%m-%d")
            elif input_type != "number":
                text = text.lower()
                element[i] = element[i].lower()

            if (operator == "not like" and ops["like"](element[i], text)) \
                    or (operator != "not like" and not ops[operator](element[i], text)):
                new_file_name = file_name_2
            else:
                new_file_name = file_name_1

            with open(path + new_file_name, "a", encoding="utf-8") as file:
                    csv.writer(file).writerow(self.read_element(index))

        add_file(file_name_1, file_display_1, self.file_type, self.get_type())
        add_file(file_name_2, file_display_2, self.file_type, self.get_type())
        os.remove(path + file_name)
        
    def merge(self, other_file_name):
        path = read_config()[self.get_type()]

        count = 0

        if not "--" in self.file_name:
            new_file_name = self.file_name
        elif not "--" in other_file_name:
            new_file_name = other_file_name
        else:
            new_file_name = self.file_name.split("--")[0] + ".csv"
            while file_in_meta(new_file_name, self.get_type()):
                new_file_name = self.file_name + "--" + str(count) + ".csv"
                count += 1

        new_file_display = get_file_display(self.file_name, self.get_type()).split("--")[0].strip() \
            + (" -- " + str(count) if count else "")

        old_files = [file_name for file_name in [self.file_name, other_file_name] if file_name != new_file_name]

        for file_name in old_files:
            with open(path + file_name, "r", encoding="utf-8") as input, \
                    open(path + new_file_name, "a", encoding="utf-8") as output:
                for line in input:
                    output.write(line)

            os.remove(path + file_name)

        add_file(new_file_name, new_file_display, self.file_type, self.get_type())
        
        self.merged_file_name = new_file_name
        return new_file_name

    def column_values(self, column):
        values = set()
        index = self.get_attribute_index(column)
        for row in self.data:
            values.add(row[index])
        return sorted(values)
