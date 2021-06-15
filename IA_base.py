from abc import ABC, abstractmethod
from unita import *


class AI_base(ABC):
    def __init__(self):
        self.attore = None

    # TODO rimuovere l'if
    def connetti_attore(self, actor):
        if not actor:
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
        :param phase: La percentuale di svolgimento dello status da 0 a 1
        """
        pass
