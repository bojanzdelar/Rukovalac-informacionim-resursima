import tempfile
import operator
import os 

class ExternalMergeSort:
    def __init__(self, path, file_name, split_size, sort_indexes):
        self.path = path
        self.file_name = file_name
        self.split_size = split_size
        self.sort_indexes = sort_indexes
        self.temp_files = []

    def sort(self):
        self.split()
        self.merge()
    
    def split(self):
        buffer = []
        size = 0
        with open(self.path + self.file_name, "r", encoding="utf-8") as file:
            line = file.readline()
            while line:
                buffer.append(line.split(","))
                size += 1
                if size % self.split_size == 0:
                    self.create_temp_file(buffer)
                    buffer=[]
                line = file.readline()
        self.create_temp_file(buffer)

    def create_temp_file(self, buffer):
        buffer.sort(key = operator.itemgetter(*self.sort_indexes))
        for i, item in enumerate(buffer):
            buffer[i] = ",".join(item)
        temp_file = tempfile.NamedTemporaryFile(mode="w+", dir=self.path)
        temp_file.writelines(buffer)
        temp_file.seek(0)
        self.temp_files.append(temp_file)

    def merge(self):
        list = []
        for temp_file in self.temp_files:
            item = temp_file.readline()
            list.append(item)
     
        with open(self.path + self.file_name, "w", encoding="utf-8") as file:
            while True:
                min, index = None, -1
                for i, item in enumerate(list):
                    if item == "":
                        item = None
                    else:
                        item = item.split(",")
                    if min is None or self.is_smaller(item, min):
                        min, index = item, i
                if min is None:
                    break
                file.write(",".join(min))
                list[index] = self.temp_files[index].readline()

    def is_smaller(self, a, b):
        if not a or not b:
            return False
        for index in self.sort_indexes:
            if a[index] < b[index]:
                return True
            elif a[index] > b[index]:
                return False
        return False