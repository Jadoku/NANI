from random import random
from typing import Tuple

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

    def builder(self, builder_function):
        pavimento = builder_function()
        total_size = len(pavimento)*len(pavimento[0])
        current = 0
        from Pavimento import Pietra, Acqua
        for y in range(len(pavimento[0])):
            for x in range(len(pavimento)):
                if pavimento[x][y] > 0:
                    self.add_move(x, y, Pietra(), add=True)
                else:
                    pass
                    #self.add_move(x, y, Acqua(), add=True)
                current += 1
                print("\rCostruzione pavimento...", round((current/total_size)*100), end="")
        print("")
        muri = builder_function()
        total_size = len(muri) * len(muri[0])
        current = 0
        from Muro import Muro_base, Muro_ossidiana
        for y in range(len(muri[0])):
            for x in range(len(muri)):
                if muri[x][y] > 0:
                    self.add_move(x, y, Muro_base(), add=True)
                else:
                    pass
                    # self.add_move(x, y, Muro_ossidiana(), add=True)
                current += 1
                print("\rCostruzione muri...", round((current / total_size)*100), end="")

        print("\nCostruzione risorse... da finire")
        # TODO finire di costruire le risorse

    def perlin_builder(self, size: Tuple[int, int], octave=10, seed=1, threshold=-2):
        from perlin_noise import PerlinNoise
        noise = PerlinNoise(octaves=octave, seed=seed)
        xpix, ypix = size
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

        if threshold != -2:
            for cy in range(xpix):
                for cx in range(ypix):
                    pic[cx][cx] = int(pic[cx][cy] >= threshold)
        return pic

    def life_builder(self, size, cicles=5, life=(2, 3), death=(1, 4, 5, 6, 7, 8), born=(3,), count=1, mask=0,
                     only_ortogonal=False, render_alive="██", render_dead="░░"):
        # Creo la matrice
        matrix = []
        result = []
        for r in range(size[0]):
            row = []
            rrow = []
            for c in range(size[1]):
                row.append(round(random()))
                rrow.append(0)
            matrix.append(row)
            result.append(rrow)

        # creo la funzione che mi conta i vicini di ogni cella
        def vicini(x, y):
            coords = [
                (-1, -1), (0, -1), (1, -1),
                (-1, 0),           (1, 0),
                (-1, 1), (0, 1),   (1, 1)
            ]
            if only_ortogonal:
                coords = [
                             (0, -1),
                    (-1, 0),         (1, 0),
                              (0, 1)
                ]
            res = 0
            lista_vicini = []
            for cr in coords:
                nx, ny = x + cr[0], y + cr[1]
                if 0 <= nx < size[0] and 0 <= ny < size[1]:
                    # se le coordinate dei vicini sono nei bordi
                    if matrix[nx][ny] == 1:
                        # se uguali a 1 (vive) conta il vicino
                        res += 1
                        lista_vicini.append(matrix[nx][ny])
            return res, lista_vicini

        # Si fanno i cicli e si guarda come evolvono
        for cile in range(cicles):
            # creo una matrice vuota che sarà la mia nuova matrix modificata
            support = []
            # Esploro ogni casella della matrice
            for cy in range(size[1]):
                row = []
                for cx in range(size[0]):
                    u = matrix[cx][cy]
                    v, l = vicini(cx, cy)
                    nu = u
                    if u == 1:
                        if v in life:
                            result[cx][cy] = 1 if count == 1 else result[cx][cy]
                            nu = 1
                        elif v in death:
                            result[cx][cy] = 1 if count == 0 else result[cx][cy]
                            nu = 0
                    else:
                        if v in born:
                            result[cx][cy] = 1 if count == -1 else result[cx][cy]
                            nu = 1
                    result[cx][cy] = 1 if 0 < mask == v else result[cx][cy]
                    result[cx][cy] = 0 if 0 > mask and abs(mask) == v else result[cx][cy]
                    row.append(nu)
                support.append(row)
            matrix = support
        return matrix


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
