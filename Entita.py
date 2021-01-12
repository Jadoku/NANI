from abc import ABC
from Oggetto import *

class Entita(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.vita = 10
        self.ferite = 0
        self.attacco = 0
        self.percezione = 1
        self.risorsa = []
        self.slot_inventario = 1
        self.categoria = Cat.Entita

    def add_inventario(self, risorsa):
        if len(self.risorsa) < self.slot_inventario:
            self.risorsa.append(risorsa)

