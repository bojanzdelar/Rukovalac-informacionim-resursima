class Student:
    def __init__(self, ustanova, broj_indeksa, prezime, ime):
        self.ustanova = ustanova
        self.broj_indeksa = broj_indeksa
        self.prezime = prezime
        self.ime = ime

    def serialize(self):
        return self.ustanova + ";" + self.broj_indeksa + ";" + self.prezime + ";" + self.ime

    @staticmethod
    def deserialize(line):
        data = line.split(";")
        return Student(data[0], data[1], data[2], data[3])

    @staticmethod
    def load():
        studenti = []
        with open("data/student.csv") as file:
            for line in file:
                studenti.append(Student.deserialize(line.strip()))
        return studenti