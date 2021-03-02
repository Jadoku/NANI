from random import randrange

from Entita import *
from Risorsa import Sassi


class Muro(ABC,Entita):
    def __init__(self):
        super().__init__()
        self.nascosto: bool = True

    def get_damage(self,danno,attaccante=None):
        super().get_damage(danno)
        for _ in range(danno):
            self.mappa.add_move(attaccante.x,attaccante.y,Sassi(),add=True)


class Muro_base(Muro):
    def __init__(self):
        super().__init__()
        self.vita = randrange(10, 20)
        self.nome = "Roccia"

class Muro_ossidiana(Muro):
    def __init__(self):
        super().__init__()
        self.vita = -1
        self.nome = "Ossidiana"
