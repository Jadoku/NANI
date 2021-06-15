import time
from abc import ABC, abstractmethod
from random import randrange

from Muro import Muro_base
from Risorsa import Erbe, Cristallo
from unita import Unita


class Nano(Unita, ABC):
    def __init__(self, AI, sprite, vita, attacco, percezione, inventario):
        super().__init__(AI)
        self.vita = vita
        self.attacco = attacco
        self.percezione = percezione
        self.slot_inventario = inventario
        self.livello = 0
        self.sprite = sprite

    def avanzamento_livello(self):
        self.livello += 1
        self.vita += 5
        self._level_up()

    @abstractmethod
    def _level_up(self):
        pass


class Minatore(Nano):
    def __init__(self, AI):
        super().__init__(AI, "minatore", 100, 2, 1, 5)

    def esegui(self, target, *agrs):
        if isinstance(target, Muro_base):
            self._attacca(target)

    def _level_up(self):
        self.slot_inventario += 1
        self.attacco += 1


class Guardia(Nano):
    def __init__(self, AI):
        super().__init__(AI,"guardia", 100, 10, 1, 1)

    def esegui(self, target, *args):
        if isinstance(target, Unita):
            self._attacca(target)

    def _level_up(self):
        self.attacco += 5
        self.vita += 5


class Cerusico(Nano):
    def __init__(self, AI):
        super().__init__(AI,"cerusico", 100, 2, 1, 5)

    def esegui(self, target, *args):
        if isinstance(target, Unita) and any(isinstance(x, Erbe) for x in self.inventario):
            time.sleep(2)
            for x in self.inventario:
                if isinstance(x, Erbe):
                    del x
                    break
            target.ferite -= min(50 + 5 * self.livello, target.ferite)

    def _level_up(self):
        pass


class Prospettore(Nano):
    def __init__(self, AI):
        super().__init__(AI, "prospettore", 100, 2, 1, 1)

    def esegui(self, target, *args):
        if args[0] == "prospezione" and isinstance(target, Muro_base):
            target.carotami()
        if args[0] == "impianto" and any(isinstance(x, Cristallo) for x in self.inventario) and len(
                target.inventario) == 1:
            for x in self.inventario:
                if isinstance(x, Cristallo):
                    if randrange(1, 10) > min(self.livello, 5):
                        del x
                    break
            target.inventario.append(target.contenuto().copy())

    def _level_up(self):
        pass


'''
class Carpentiere(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,2,1,1)

minatore
guardia
carpentiere
cerusico
prospettore
'''
