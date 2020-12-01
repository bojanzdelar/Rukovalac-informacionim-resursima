class VisokoskolskaUstanova:
    def __init__(self, oznaka, naziv, adresa, studenti=[]):
        self.oznaka = oznaka
        self.naziv = naziv
        self.adresa = adresa
        self.studenti = studenti # FIXME: privremeno