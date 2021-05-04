from abc import ABC, abstractmethod
from Oggetto import *


class Entita(Oggetto, ABC):
    def __init__(self):
        super().__init__()
        self.vita = 10
        self.ferite = 0
        self.attacco = 0
        self.percezione = 1
        self.inventario = []
        self.slot_inventario = 1

    def get_damage(self, danno, attaccante=None):
        self.ferite += danno
        if self.ferite >= self.vita:
            self.on_death()

    def on_death(self):
        self.mappa.remove_item(self)
