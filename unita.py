import time
from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread

import Pannello_controllo as pc
from Entita import Entita
from IA_base import AI_base
from Risorsa import Risorsa


class Status(Enum):
    """
    Stati ed attività del personaggio
    """
    INATTIVO = 0
    MOVIMENTO = 1
    ATTACCO = 2
    RACCOLTA = 3
    USO_FORZIERE = 4
    AZIONE = 5


class Phase(Enum):
    START = 0
    ACTIVE = 0.5
    FINISH = 1

    """
    Errori da passare come phase del comando
    """
    # 100-199 Errori movimento
    NESSUNA_DESTINAZIONE = 100
    PERCORSO_INACCESSIBILE = 101
    # 200-299 Errori attacco
    BERSAGLIO_FUORI_RANGE = 200
    # 300-399 Errori raccolta
    TENTATA_RACCOLTA_NON_RISORSA = 300
    INVENTARIO_PIENO = 301
    RISORSA_FUORI_RANGE = 302
    # 400-499 Errori forziere
    FORZIERE_FUORI_PORTATA = 400
    RISORSA_MANCANTE = 401
    RISORSA_DA_DEPOSITARE_NON_POSSEDUTA = 402
    # 500-599 Errori azione
    BERSAGLIO_AZIONE_FUORI_PORTATA = 500


class Unita(Entita, ABC, Thread):
    def __init__(self, IA):
        super(Unita, self).__init__()
        Thread.__init__(self)
        self.z = pc.z_unita
        self.movimento = 1
        self.ia: AI_base = IA
        self.ia.connetti_attore(self)
        self.portata = 1
        self.mod_movimento = 1
        self.percorso = []
        self.lunghezza_percorso = 0
        self.destinazione = None
        self.forziere = None
        self.status = Status.INATTIVO  # Il segnale è cosa sta facendo l'unità
        self.status_phase: Phase = Phase.ACTIVE
        # La fase del segnale è il suo svolgimento Start, acting, finish
        # Questo per avere una graduatoria sullo svolgimento dell'operazione

    def on_map_enter(self, mappa):
        super().on_map_enter(mappa)
        self.forziere = mappa.forziere

    def run(self):
        self._set_status(Status.INATTIVO, Phase.START)
        while True:  # self.ferite < self.vita: TODO mettere una fine del processo
            self.ia.comando()

    def _set_status(self, new_status: Status = None, new_phase: Phase = None, messaggio: str = ""):
        """
        Imposta il nuovo status e notifica alla ai il combiamento

        :param new_status: il nuovo segnale
        :param new_phase: la nuova fase
        :param messaggio: debug dello status
        """
        if (new_status is not None) and new_status != self.status:
            self.status = new_status
        if (new_phase is not None) and new_phase != self.status_phase:
            self.status_phase = new_phase
        self.ia.unit_status_update(self.status, self.status_phase, messaggio)

    def passa_turno(self):
        self._set_status(Status.INATTIVO, Phase.START)

    def imposta_destinazione(self, nuova_destinazione):
        new_path = peso, percorso, distanza = self.distanza(nuova_destinazione)
        if distanza > 1:
            self._set_status(Status.MOVIMENTO, Phase.START, new_path)
        elif 0 <= distanza <= 1:
            self._set_status(Status.MOVIMENTO, Phase.FINISH, new_path)
            return
        else:
            self._set_status(Status.MOVIMENTO, Phase.PERCORSO_INACCESSIBILE, new_path)
            return
        self.percorso = percorso
        self.lunghezza_percorso = max(distanza-1, 0)

    def muovi(self):
        if self.percorso:
            self._set_status(Status.MOVIMENTO, Phase.ACTIVE)
            coord = self.percorso.pop(0)
            print("coordinata", coord)
            peso = self.mappa.add_move(coord[0], coord[1], self)
            time.sleep(peso / 3)
        elif not self.percorso:
            self._set_status(Status.MOVIMENTO, Phase.FINISH)
        else:
            print("Comando muovi usato senza destinazione")
            self._set_status(Status.MOVIMENTO, Phase.NESSUNA_DESTINAZIONE)

    def _attacca(self, bersaglio):
        self._set_status(Status.ATTACCO, Phase.START)
        if self.in_range(bersaglio):
            self._deal_damage(self.attacco)
            self._set_status(Status.ATTACCO, Phase.FINISH)
        else:
            msg = "port: "+str(self.portata)+", "+"pos: "+str((self.x, self.y))+", "+"tgt "+str((bersaglio.x, bersaglio.y))
            self._set_status(Status.ATTACCO, Phase.BERSAGLIO_FUORI_RANGE, msg)

    def _deal_damage(self, bersaglio):
        bersaglio.get_damage(self.attacco, self)
        time.sleep(0.5)

    def raccogli(self, target, da_mappa=True):
        """
        aggiunge un oggetto all'inventario di una unità

        :param target: oggetto da raccogliere
        :param da_mappa: indica se l'oggetto da raccogliere è per terra (True) o no (False)
        :return:
        """
        self._set_status(Status.RACCOLTA, Phase.START)
        if isinstance(target, Risorsa):
            if self.in_range(target):
                if len(self.inventario) < self.slot_inventario:
                    self.inventario.append(target)
                    if da_mappa:
                        self.mappa.remove_item(target)
                    time.sleep(0.2)
                    self._set_status(Status.RACCOLTA, Phase.FINISH)
                else:
                    self._set_status(Status.RACCOLTA, Phase.INVENTARIO_PIENO)
            else:
                self._set_status(Status.RACCOLTA, Phase.RISORSA_FUORI_RANGE)
        else:
            self._set_status(Status.RACCOLTA, Phase.TENTATA_RACCOLTA_NON_RISORSA)

    def in_range(self, bersaglio):
        return max(abs(self.x - bersaglio.x), abs(self.y - bersaglio.y)) <= self.portata
        # return self.portata >= self.distanza(bersaglio)[2] > 0

    def azione(self, target):
        self._set_status(Status.AZIONE, Phase.START)
        if self.in_range(target):
            self.esegui(target)
            self._set_status(Status.AZIONE, Phase.FINISH)
        else:
            msg = "port: " + str(self.portata) + ", " + "pos: " + str((self.x, self.y)) + ", " + "tgt " + str(
                (target.x, target.y))
            self._set_status(Status.AZIONE, Phase.BERSAGLIO_AZIONE_FUORI_PORTATA, msg)
            pass

    def usa_forziere(self, preleva: pc.nomi_risorse = None, deposita: Risorsa = None):
        self._set_status(Status.USO_FORZIERE, Phase.START)
        if not self.in_range(self.forziere):
            self._set_status(Status.USO_FORZIERE, Phase.FORZIERE_FUORI_PORTATA)
            return
        if preleva:
            if self.forziere.has_item(preleva.value):
                self.forziere.pick_item(preleva.value, self)
                self._set_status(Status.USO_FORZIERE, Phase.FINISH)
            else:
                self._set_status(Status.USO_FORZIERE, Phase.RISORSA_MANCANTE)
        elif deposita:
            if deposita in self.inventario:
                self.forziere.drop_item(deposita)
                self.inventario.remove(deposita)
            else:
                self._set_status(Status.USO_FORZIERE, Phase.RISORSA_DA_DEPOSITARE_NON_POSSEDUTA)

    @abstractmethod
    def esegui(self, target, *args):
        pass
