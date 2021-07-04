from abc import ABC, abstractmethod
from random import choice


class AI_base(ABC):

    def __init__(self):
        self.attore = None

    def connetti_attore(self, actor):
        self.attore = actor

    @abstractmethod
    def comando(self):
        """
        Definisce il comando che dovrà eseguire l'attore
        """
        pass

    @abstractmethod
    def unit_status_update(self, status, phase):
        """
        Semplice observer che notifica il cambio di status dell'attore

        :param status: Lo status cambiato dell'attore
        :param phase: Il codice di svolgimento dell'azione o dell'errore
        """
        pass


class AI_placeholder(AI_base):

    def comando(self):
        pass

    def unit_status_update(self, status, phase):
        pass


class AI_minatore(AI_base):
    """
    Muove e mina senza fare altro
    """

    def __init__(self):
        super().__init__()
        self.target = None
        self.move = True
        self.mine = False

    def comando(self):
        print("Minatore", self.target, self.move, self.mine)
        if self.move:
            print("Minatore muove")
            self.attore.muovi()
        if self.mine:
            if self.target:
                print("Minatore mina")
                self.attore.azione(self.target)
            else:
                print("minatore ha finito di minare")
                self.attore.passa_turno()

    def unit_status_update(self, status, phase):
        print("Minatore:", status.name, phase.name)
        from unita import Status, Phase
        if status == Status.INATTIVO or Phase.NESSUNA_DESTINAZIONE or Phase.PERCORSO_INACCESSIBILE:
            self.mine = False
            self.move = False
            # Se inattivo, si mette a cercare un oggetto da minare a caso
            from Muro import Muro_base
            self.target = choice(self.attore.mappa.get_interactable(filter_by=Muro_base))
            self.attore.imposta_destinazione(self.target)
        if status == Status.MOVIMENTO and phase == Phase.START:
            self.move = True
        if status == Status.MOVIMENTO and phase == Phase.FINISH:
            self.move = False
            self.mine = True
