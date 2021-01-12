from Oggetto import *


class Pavimento(ABC, Oggetto):
    def __init__(self):
        super().__init__()
        self.categoria = Cat.Pavimento

    def get_name(self):
        return self.__class__.__name__

class Pietra(Pavimento):
    def __init__(self):
        self.nome = self.get_name()
        self.mod_movimento = 1

class Acqua(Pavimento):
    def __init__(self):
        self.nome = self.get_name()
        self.mod_movimento = 2

class Lava(Pavimento):
    def __init__(self):
        self.nome = self.get_name()
        self.mod_movimento = 0