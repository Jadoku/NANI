from random import randrange

from Entita import *
from Risorsa import Sassi


class Muro(Entita, ABC):
    def __init__(self, sprite: str):
        super().__init__()
        self.sprite = sprite

    def get_damage(self, danno, attaccante=None):
        super().get_damage(danno)
        for _ in range(danno):
            self.mappa.add_move(attaccante.x, attaccante.y, Sassi(), add=True)


class Muro_base(Muro):
    def __init__(self):
        super().__init__("muro")
        self.controllato: bool = False
        self.vita = randrange(10, 20)
        self.nome = "Roccia"

    def carotami(self):
        self.controllato = True
        if not self.inventario:
            self.nome = "Riserva di " + self.inventario[0].nome
        else:
            return "Blocco di granito"

    def contenuto(self):
        if self.controllato and not self.inventario:
            return self.inventario[0]
        else:
            return []


class Muro_ossidiana(Muro):
    def __init__(self):
        super().__init__("ossidiana")
        self.vita = -1
        self.nome = "Ossidiana"
