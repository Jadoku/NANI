from abc import ABC, abstractmethod
from Entita import Entita
from Risorsa import Risorsa


class Unita(Entita, ABC):
    def __init__(self,IA):
        super().__init__()
        self.movimento = 1
        self.ai = IA
        self.portata = 1
        self.mod_movimento = 1

    def muovi(self,X,Y):
        self.mappa.add_move(X,Y,self)

    def attacca(self,bersaglio):
        bersaglio.get_damage(self.attacco,self)

    def raccogli(self,target):
        if len(self.inventario) < self.slot_inventario and isinstance(target, Risorsa):
            self.inventario.append(self.mappa.remove_item(target))


    @abstractmethod
    def esegui(self,target):
        pass