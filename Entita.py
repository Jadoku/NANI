from abc import ABC


class Entita(ABC):
    def __init__(self):
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

    def add_inventario(self,risorsa):
        if len(self.risorsa) < self.slot_inventario:
            self.risorsa.append(risorsa)

