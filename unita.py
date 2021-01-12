from abc import ABC
from Entita import Entita
from Oggetto import Cat

class Unita(Entita, ABC):
    def __init__(self):
        super().__init__()
        self.movimento = 1