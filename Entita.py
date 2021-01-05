from abc import ABC
from Oggetto import Oggetto


class Entita(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.nome = ""
        self.vita = 10
        self.ferite = 0
        self.movimento = 1
        self.attacco = 0
        self.percezione = 1
        self.posizione = []
        self.priorita = 0
        self.risorsa = []
        self.slot_inventario = 1
        self.z = 0

    def add_inventario(self, risorsa):
        if len(self.risorsa) < self.slot_inventario:
            self.risorsa.append(risorsa)

