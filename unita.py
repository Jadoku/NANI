from abc import ABC, abstractmethod
from Entita import Entita
from Oggetto import Cat

class Unita(Entita, ABC):
    def __init__(self,IA,mappa):
        super().__init__()
        self.movimento = 1
        self.ai = IA
        self.mappa = mappa
        self.portata = 1

    def muovi(self,X,Y):
        self.mappa.add_move(X,Y,self)

    def attacca(self,bersaglio):
        bersaglio.get_damage(self.attacco)

    def raccogli(self):
        pass

    @abstractmethod
    def esegui(self,target):
        pass