from abc import ABC, abstractmethod
from unita import Unita, Status, Phase, Error


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
