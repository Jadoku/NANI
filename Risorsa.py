from Oggetto import *
import Pannello_controllo as pc


class Risorsa(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.mod_movimento = pc.mod_movimento_risorse
        self.z = pc.z_risorse

    def get_name(self):
        return self.__class__.__name__


class Sassi(Risorsa):
    def __init__(self):
        super().__init__()
        self.nome = self.get_name()
        self.sprite = "sassi"


class Ferro(Risorsa):
    def __init__(self):
        super().__init__()
        self.nome = self.get_name()
        self.sprite = "ferro"


class Zolfo(Risorsa):
    def __init__(self):
        super().__init__()
        self.nome = self.get_name()
        self.sprite = "zolfo"


class Cristallo(Risorsa):
    def __init__(self):
        super().__init__()
        self.nome = self.get_name()
        self.sprite = "cristallo"


class Erbe(Risorsa):
    def __init__(self):
        super().__init__()
        self.nome = self.get_name()
        self.sprite = "erbe"
