from abc import ABC, abstractmethod
from Entita import Entita
from Oggetto import Cat

class Unita(Entita, ABC):
    def __init__(self):
        super().__init__()
        self.movimento = 1
        self.ai = None

    def muovi(self):
        pass

    def attacca(self):
        pass

    @abstractmethod
    def esegui(self,target):