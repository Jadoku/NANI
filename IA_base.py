from abc import ABC, abstractmethod
from typing import Final


class AI_base(ABC):
    def __init__(self):
        self.attore = None

    @Final
    def connetti_attore(self, actor):
        self.attore = actor

    @abstractmethod
    def comando(self):
        pass