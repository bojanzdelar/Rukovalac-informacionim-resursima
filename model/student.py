class Student:
    def __init__(self, ustanova, broj_indeksa, prezime, ime):
        self.data = {
            "Ustanova" : ustanova,
            "Broj indeksa" : broj_indeksa,
            "Prezime" : prezime,
            "Ime" : ime
        }

    def serialize(self):
        return self.data["Ustanova"] + ";" + self.data["Broj indeksa"] + ";" + self.data["Prezime"] + ";" + self.data["Ime"]

    @staticmethod
    def deserialize(line):
        data = line.split(";")
        return Student(data[0], data[1], data[2], data[3])
        
    @staticmethod
    def load():
        studenti = []
        with open("data/studenti.csv") as file:
            for line in file:
                studenti.append(Student.deserialize(line.strip()))
        return studenti