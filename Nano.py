from abc import ABC

from Muro import Muro_base
from unita import Unita


class Nano(Unita,ABC):
    def __init__(self,AI,vita,attacco,percezione,inventario):
        super().__init__(AI)
        self.vita = vita
        self.attacco = attacco
        self.percezione = percezione
        self.slot_inventario = inventario


class Minatore(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,2,1,5)

    def esegui(self, target):
        if isinstance(target,Muro_base):
            self.attacca(target)


class Guardia(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,10,1,1)

    def esegui(self, target):
        if isinstance(target,Unita):
            self.attacca(target)

class Cerusico(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,2,1,5)


class Prospettore(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,2,1,1)

'''
class Carpentiere(Nano):
    def __init__(self,AI):
        super().__init__(AI,100,2,1,1)
'''

'''
minatore
guardia
carpentiere
cerusico
prospettore
'''