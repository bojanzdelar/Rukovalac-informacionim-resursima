from model.student import Student

class VisokoskolskaUstanova:
    def __init__(self, oznaka, naziv, adresa):
        self.oznaka = oznaka
        self.naziv = naziv
        self.adresa = adresa
        # Kada sam u konstruktor stavio default parametar studenti=[], sve instance ove
        # klase su imale zajednicku adresu za atribut studenti
        self.studenti = [] # FIXME: privremeno 

    def serialize(self):
        return self.oznaka + ";" + self.naziv + ";" + self.adresa

    @staticmethod
    def deserialize(line):
        data = line.split(";")
        return VisokoskolskaUstanova(data[0], data[1], data[2])

    @staticmethod
    def load():
        ustanove = []
        with open("data/visokoskolske_ustanove.csv") as file:
            for line in file:
                ustanove.append(VisokoskolskaUstanova.deserialize(line.strip()))
        studenti = Student.load()
        for student in studenti:
            for ustanova in ustanove:
                if student.ustanova == ustanova.oznaka:
                    ustanova.studenti.append(student)
                    break
        return ustanove