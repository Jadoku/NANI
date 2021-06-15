from abc import ABC, abstractmethod
from enum import Enum

from Entita import Entita
from IA_base import AI_base
from Risorsa import Risorsa
from threading import Thread
import time


class Segnale(Enum):
    INCOSCENTE = -1
    INATTIVO = 0
    MOVIMENTO = 1
    ATTACCO = 2
    RACCOLTA = 3
    AZIONE = 4


class Unita(Entita, ABC, Thread):
    def __init__(self, IA):
        super().__init__()
        self.z = 3
        self.movimento = 1
        self.ia: AI_base = IA
        # self.ia.connetti_attore(self)
        self.portata = 1
        self.mod_movimento = 1
        self.percorso = []
        self.destinazione = None
        self.status = Segnale.IDLE  # Il segnale è cosa sta facendo l'unità
        self.status_phase = 0  # La fase del segnale è il suo svolgimento 0 inizio >0 esecuzione 1 fine
        # Questo per avere una graduatoria sullo svolgimento dell'operazione

    def run(self):
        while self.ferite < self.vita:
            pass
            # TODO AI_base.comando()

    def _set_status(self, new_status: Segnale = None, new_phase: int = -1):
        """
        Imposta il nuovo status e notifica alla ai il combiamento
        :param new_status: il nuovo segnale
        :param new_phase: la nuova fase
        """
        if not new_status and new_status != self.status:
            self.status = new_status
        if new_phase > -1 and new_phase != self.status_phase:
            self.status_phase = new_phase
        self.ia.unit_status_update(self.status, self.status_phase)

    def muovi(self, nuova_destinazione=None):
        if not nuova_destinazione:
            if self.destinazione != nuova_destinazione:
                self.percorso = self.distanza(nuova_destinazione)[1]
        elif self.percorso:
            coord = self.percorso.pop(0)
            peso = self.mappa.add_move(coord[0], coord[1], self)
            time.sleep(peso / 3)
        else:
            print("Comando muovi usato senza destinazione")

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
            time.sleep(1)
        else:
            pass

    @abstractmethod
    def esegui(self, target, *args):
        pass
