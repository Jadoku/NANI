from abc import ABC, abstractmethod


class AI_base(ABC):
    def __init__(self):
        self.attore = None

    # TODO rimuovere l'if
    def connetti_attore(self, actor):
        if not actor:
            self.attore = actor

    @abstractmethod
    def comando(self):
        pass
