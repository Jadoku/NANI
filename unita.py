from abc import ABC, abstractmethod
from Entita import Entita
from IA_base import AI_base
from Risorsa import Risorsa
from threading import Thread
import time


# TODO sistema di segnali con enum

class Unita(Entita, ABC, Thread):
    def __init__(self, IA):
        super().__init__()
        self.movimento = 1
        self.ia = IA
        self.ia.connetti_attore(self)
        self.portata = 1
        self.mod_movimento = 1
        self.percorso = []
        self.destinazione = None

    def run(self):
        while self.ferite < self.vita:
            AI_base.comando()

    def muovi(self, destinazione):
        if not self.percorso or destinazione is not self.destinazione:
            self.percorso = self.distanza(destinazione)[1]
        else:
            coord = self.percorso.pop(0)
            peso = self.mappa.add_move(coord[0], coord[1], self)
            time.sleep(peso / 3)

    def _attacca(self, bersaglio):
        if self.in_range(bersaglio):
            bersaglio.get_damage(self.attacco, self)
            time.sleep(0.5)
        else:
            pass

    def raccogli(self, target, da_mappa=True):
        """
        aggiunge un oggetto all'inventario di una unità
        :param target: oggetto da raccogliere
        :param da_mappa: indica se l'oggetto da raccogliere è per terra (True) o no (False)
        :return:
        """
        if self.in_range(target) and len(self.inventario) < self.slot_inventario and isinstance(target, Risorsa):
            self.inventario.append(target)
            if da_mappa:
                self.mappa.remove_item(target)
            time.sleep(0.2)

    def in_range(self, bersaglio):
        return len(self.distanza(bersaglio)[1]) <= self.portata

    def azione(self, target):
        if self.in_range(target):
            self.esegui(target)
        else:
            pass

    @abstractmethod
    def esegui(self, target, *args):
        pass
