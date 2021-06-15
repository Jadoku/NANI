from Entita import Entita
from Oggetto import Oggetto
from Risorsa import Risorsa


class Livello:
    def __init__(self, lato: int = 31):
        # self.matrix=[[[0,0,0]]*lato for _ in range(lato)]
        self.lista_oggetti = []
        self.lato = lato

    def matrix(self, phase=False):
        """
        popola la matrice con blocchi e pesi. se l'unità ignora i muri passa phase=True
        :return: matrice con blocchi o pesi
        """
        matrix = []
        for i in range(self.lato):
            r = []
            for j in range(self.lato):
                if phase:
                    r.append(1)
                else:
                    r.append(self.is_accessible(i, j))
            matrix.append(r)
        return matrix

    def get_coord(self, x, y, visuale=True):
        if visuale:
            return list(filter(lambda n: n.x == x and n.y == y and n.visibile, self.lista_oggetti))
        else:
            return list(filter(lambda n: n.x == x and n.y == y, self.lista_oggetti))

    def is_accessible(self, x, y):
        """
        controlla se una casella è bloccante
        :param x: coordinata X
        :param y: coordinata Y
        :return: 0 se bloccante, altrimenti modificatore di movimento.
        """
        k = 0
        lista = self.get_coord(x, y)
        if not lista:
            return -1
        for i in lista:
            if i.mod_movimento == 0:
                return 0
            else:
                k += i.mod_movimento
        return max(k, 0)

    def add_move(self, x, y, oggetto, add: bool = False, phase: bool = False):
        """
        aggiunge o muove un oggetto all'interno della griglia
        :param x: destinazione x
        :param y: destinazione y
        :param oggetto: oggetto da muovere o aggiungere
        :param add: se true, aggiunge un oggetto non presente sulla griglia
        :param phase: ignora se il terreno è bloccante o meno
        :return: 0 se non è possibile, peso della casella di destinazione se possibile
        """
        peso = self.is_accessible(x, y)
        if self.check_bounds(x, y) and (bool(peso) or phase):
            oggetto.x = x
            oggetto.y = y
            if add:
                self.lista_oggetti.append(oggetto)
                oggetto.mappa = self
                self.lista_oggetti.sort(key=lambda x: x.z)
            return peso
        else:
            print("non puoi aggiungere/muovere un oggetto in una casella occupata")
            return 0

    def remove_item(self, oggetto):
        self.lista_oggetti.remove(oggetto)
        if isinstance(oggetto, Entita):
            for i in oggetto.inventario:
                self.add_move(oggetto.x, oggetto.y, i, True)
        return oggetto

    def check_bounds(self, x, y):
        return (0 <= x < self.lato) and (0 <= y < self.lato)

    def builder(self,):
        from perlin_noise import PerlinNoise
        noise = PerlinNoise(octaves=10, seed=1)

class Forziere(Oggetto):
    def __init__(self):
        super().__init__()
        self.visibile = True
        self.lista_risorse = {
            "Zolfo": 0,
            "Ferro": 0,
            "Erbe": 0,
            "Cristallo": 0,
            "Sassi": 0
        }

    def drop_item(self, item: Risorsa, donatore):
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
