from Oggetto import *


class Risorsa(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.mod_movimento = 0.2
        self.z = 1

    def get_name(self):
        return self.__class__.__name__


class Sassi(Risorsa):
    def __init__(self):
        self.nome = self.get_name()


class Ferro(Risorsa):
    def __init__(self):
        self.nome = self.get_name()


class Zolfo(Risorsa):
    def __init__(self):
        self.nome = self.get_name()


class Cristallo(Risorsa):
    def __init__(self):
        self.nome = self.get_name()


class Erbe(Risorsa):
    def __init__(self):
        self.nome = self.get_name()
