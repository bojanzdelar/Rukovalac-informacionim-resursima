from model.student import Student

class VisokoskolskaUstanova:
    def __init__(self, oznaka, naziv, adresa):
        self.data = {
            "Oznaka": oznaka,
            "Naziv": naziv,
            "Adresa": adresa
        }
        self.list = [] # FIXME: privremeno 

    def serialize(self):
        return self.data["oznaka"] + ";" + self.data["naziv"] + ";" + self.data["adresa"]

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
        list = Student.load()
        for student in list:
            for ustanova in ustanove:
                if student.data["Ustanova"] == ustanova.data["Oznaka"]:
                    ustanova.list.append(student)
                    break
        return ustanove