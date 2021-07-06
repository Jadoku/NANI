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
        if self.move:
            self.attore.muovi()
        if self.mine:
            if self.target.ferite < self.target.vita:
                self.attore.azione(self.target)
            else:
                self.mine = False
                self.attore.passa_turno()

    def unit_status_update(self, status, phase):
        print("Minatore:", status.name, phase.name)
        from unita import Status, Phase

        inattivo = status == Status.INATTIVO

        no_dest = status == Status.MOVIMENTO and phase == Phase.NESSUNA_DESTINAZIONE
        no_perco = status == Status.MOVIMENTO and phase == Phase.PERCORSO_INACCESSIBILE

        inizio_movimento = status == Status.MOVIMENTO and phase == Phase.START
        fine_movimento = status == Status.MOVIMENTO and phase == Phase.FINISH

        if inattivo or no_dest or no_perco:
            self.mine = False
            self.move = False
            from Muro import Muro_base
            self.target = choice(self.attore.mappa.get_visible(filter_by=Muro_base))
            self.attore.imposta_destinazione(self.target)
        if inizio_movimento:
            self.move = True
        if fine_movimento:
            self.move = False
            self.mine = True
