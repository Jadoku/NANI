from Oggetto import *
import Pannello_controllo as pc


class Pavimento(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.z = pc.z_pavimento

    def get_name(self):
        return self.__class__.__name__


class Pietra(Pavimento):
    def __init__(self):
        super(Pietra, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = pc.mod_movimento_pietra
        self.sprite = "pavimento"


class Acqua(Pavimento):
    def __init__(self):
        super(Acqua, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = pc.mod_movimento_acqua
        self.sprite = "acqua"


class Lava(Pavimento):
    def __init__(self):
        super(Lava, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = pc.mod_movimento_lava
        self.sprite = "lava"
