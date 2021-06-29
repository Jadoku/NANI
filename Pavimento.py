from Oggetto import *


class Pavimento(Oggetto, ABC):
    def __init__(self):
        super().__init__()

    def get_name(self):
        return self.__class__.__name__


class Pietra(Pavimento):
    def __init__(self):
        super(Pietra, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = 1
        self.sprite = "pavimento"


class Acqua(Pavimento):
    def __init__(self):
        super(Acqua, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = 2
        self.sprite = "acqua"


class Lava(Pavimento):
    def __init__(self):
        super(Lava, self).__init__()
        self.nome = self.get_name()
        self.mod_movimento = 0
        self.sprite = "lava"
