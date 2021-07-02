from enum import Enum
from Oggetto import Oggetto
from Risorsa import Risorsa


class Forziere(Oggetto):

    def __init__(self):
        super().__init__()
        self.visibile = True
        self.sprite = "forziere"
        self.lista_risorse = {
            "Zolfo": 0,
            "Ferro": 0,
            "Erbe": 0,
            "Cristallo": 0,
            "Sassi": 0
        }

    def drop_item(self, item: Risorsa, donatore=None):
        if donatore:
            donatore.inventario.remove(item)
        self.lista_risorse[item.nome] += 1
        del item

    def pick_item(self, item_name, raccoglitore):
        if self.has_item(item_name):
            class_ = getattr(Risorsa, item_name)
            item_istance = class_()
            self.lista_risorse[item_name] -= 1
            raccoglitore.raccogli(item_istance, False)
        else:
            pass

    def get_list(self):
        return self.lista_risorse

    def has_item(self, item_name):
        return self.lista_risorse[item_name] > 0

    def get_damage(self, danno, attaccante=None):
        pass

    def on_death(self):
        pass
