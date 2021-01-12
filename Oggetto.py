from abc import ABC
from enum import Enum


class Oggetto(ABC):
    def __init__(self):
        self.x=-1
        self.y=-1
        self.categoria=0
        self.block=True
        self.mod_movimento=0
        self.priorita = 0
        self.nome = ""

class Cat(Enum):
    Oggetto = 0
    Entita = 100
    Muro = 110
    Muro_base = 111
    Muro_ossidiana = 112
    Unita = 120
    Nano = 121
    Mostro = 122
    Risorsa = 200
    Pavimento = 300
    Pavimento_pietra = 310
    Pavimento_acqua = 320
    Pavimento_lava =330