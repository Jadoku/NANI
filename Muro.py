from random import randrange

from Entita import *
from Oggetto import Cat


class Muro(ABC,Entita):
    def __init__(self):
        super().__init__()
        self.nascosto: bool = True
        self.slot_inventario = 5
        self.categoria = Cat.Muro

class Muro_base(Muro):
    def __init__(self):
        super().__init__()
        self.vita = randrange(10, 20)
        self.nome = "Roccia"
        self.categoria = Cat.Muro_base

class Muro_ossidiana(Muro):
    def __init__(self):
        super().__init__()
        self.vita = -1
        self.nome = "Ossidiana"
        self.categoria = Cat.Muro_ossidiana