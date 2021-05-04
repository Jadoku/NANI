from abc import ABC, abstractmethod
from typing import final


class AI_base(ABC):
    def __init__(self):
        self.attore = None

    @final
    def connetti_attore(self, actor):
        self.attore = actor

    @abstractmethod
    def comando(self):
        pass
