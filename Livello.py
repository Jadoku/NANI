import math
from random import random, randrange, shuffle
from typing import Tuple

import Pannello_controllo as pc
from Entita import Entita
from Forziere import Forziere


class Livello:
    def __init__(self, lato: int = 35):
        self.lista_oggetti = []
        self.lato = lato
        self.forziere = None
        self.lista_nani = []

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

    def get_coord(self, x, y, visuale=True, filter_by=None):
        if visuale:
            ret = list(filter(lambda n: n.x == x and n.y == y and n.visibile, self.lista_oggetti))
        else:
            ret = list(filter(lambda n: n.x == x and n.y == y, self.lista_oggetti))
        if filter_by:
            ret = list(filter(lambda n: isinstance(n, filter_by), ret))
        return ret

    def get_visible_list(self):
        return list(filter(lambda n: n.visibile, self.lista_oggetti))

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
                oggetto.on_map_enter(self)
                self.lista_oggetti.sort(key=lambda x: x.z)
                if isinstance(oggetto, Forziere):
                    self.forziere = oggetto
                from Nano import Nano
                if isinstance(oggetto, Nano):
                    self.lista_nani.append(oggetto)
            return peso
        else:
            print("non puoi aggiungere/muovere un oggetto in una casella occupata")
            return 0

    def remove_item(self, oggetto, destroy=False):
        self.lista_oggetti.remove(oggetto)
        if isinstance(oggetto, Entita) and not destroy:
            for i in oggetto.inventario:
                self.add_move(oggetto.x, oggetto.y, i, True)
        return oggetto

    def check_bounds(self, x, y):
        return (0 <= x < self.lato) and (0 <= y < self.lato)

    def illuminate_area(self, xx, yy, raggio=1):
        for y in range(yy - raggio, yy + raggio + 1, 1):
            for x in range(xx - raggio, xx + raggio + 1, 1):
                obj = self.get_coord(x, y, False)
                for e in obj:
                    if not e.visibile:
                        e.rivela()

    def load_percent(self, message, count=1, total=2) -> int:
        count += 1
        cur = round((count / total) * 100)
        print("\r" + message, str(cur) + "%", end="")
        if count >= total:
            print("\tOK!")
        return count

    def builder(self, resource_array=None):
        if resource_array is None:
            resource_array = pc.risorse_per_livello
        size = (self.lato, self.lato)
        pavimento = self.perlin_builder(size, octave=2, threshold=-0.2)
        total_size = size[0] * size[1]
        current = 0
        from Pavimento import Pietra, Acqua
        for y in range(len(pavimento[0])):
            for x in range(len(pavimento)):
                if int(pavimento[x][y]) > 0:
                    self.add_move(x, y, Pietra(), add=True)
                else:
                    self.add_move(x, y, Acqua(), add=True)
                current = self.load_percent("Costruzione pavimento...", current, total_size)

        muri = self.perlin_builder(size, threshold=-0.15)
        current = 0
        from Muro import Muro, Muro_base  # TODO muro di ossidiana
        for y in range(len(muri[0])):
            for x in range(len(muri)):
                if muri[x][y] > 0:
                    self.add_move(x, y, Muro_base(), add=True)
                current = self.load_percent("Costruzione muri...", current, total_size)

        # Scorro la matrice in blocchi da 5x5
        saved_points = []
        current = 0
        total_size = (size[0] // 5) * (size[1] // 5)
        for y in range(0, size[1], 5):
            for x in range(0, size[0], 5):
                # Scorre i punti scelti dall'origine x,y fino a x+w e y+h
                # e salva solo quelli con il muro
                wall_list = []
                for y1 in range(y, y + 5, 1):
                    for x1 in range(x, x + 5, 1):
                        if self.check_bounds(x1, y1):
                            if muri[x1][y1] > 0:
                                wall_list.append((x1, y1))
                if wall_list:
                    # Li mischia con il metodo shuffle
                    shuffle(wall_list)
                    # li ordina dal primo per distanza
                    source = wall_list[0]
                    wall_list.sort(key=lambda z: math.sqrt((source[0] - z[0]) ** 2 + (source[1] - z[1]) ** 2))
                    # li aggiunge ai saved points
                    saved_points.append(wall_list)
                current = self.load_percent("Calcolo distribuzione risorse...", current, total_size)

        from Risorsa import Ferro, Zolfo, Cristallo, Erbe
        resource_classes = [Ferro, Zolfo, Cristallo, Erbe]
        resource_count = resource_array
        # Inizio a scorrere la lista generata dal precedente for
        current = 0
        total_size = sum(resource_array)
        i = 0
        stop = 0
        while saved_points and resource_count:  # Esce quando una delle due liste è vuota
            # Se la lista alla posizione è piena fa l'operazione sennò la rimuove
            if saved_points[i]:
                p = saved_points[i].pop(0)
                r = randrange(0, len(resource_classes))
                inst = resource_classes[r]()
                muro = self.get_coord(p[0], p[1], False, Muro_base)[0]
                muro.inventario.append(inst)
                resource_count[r] -= 1
                if resource_count[r] == 0:
                    del resource_count[r]
                    del resource_classes[r]
            else:
                del saved_points[i]
                if not saved_points:
                    break
            # manda avanti il ciclo
            i = (i + 1) % len(saved_points)
            current = self.load_percent("Distribuzione risorse...", current, total_size)
            # Se il ciclo fa più cicli del numero di caselle lancia un errore che blocca il programma
            stop += 1
            assert stop < (size[0] * size[1])

        # creo lo spazio vuoto di inizio
        center = math.floor(size[0] / 2)
        forziere = Forziere()
        current = 0
        total_size = 25
        for y in range(center - 2, center + 3, 1):
            for x in range(center - 2, center + 3, 1):
                w = self.get_coord(x, y, False, Muro)
                if w:
                    if w[0].inventario:
                        forziere.drop_item(w[0].inventario[0], w[0])
                    self.remove_item(w[0], destroy=True)
                    current = self.load_percent("Costruzione punto partenza...", current, total_size)
        # creo il forziere
        self.add_move(center, center, forziere, add=True)
        self.load_percent("Piazzamento forziere...")
        # attivo un crawler che illumini tutte le caselle dell'inizio
        self.__start_crawler((center, center + 1))

    def __start_crawler(self, origin):
        coords = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]

        def illuminate(xx, yy):
            obj = self.get_coord(xx, yy, False)
            for e in obj:
                e.rivela()

        visited = [origin]
        i = 0
        while i < len(visited):
            cx, cy = visited[i]
            # Illumino la casella corrente
            illuminate(cx, cy)
            acc = self.is_accessible(cx, cy)
            # Aggiungo tutte le caselle adiacenti che non
            # sono in visited e se la casella di origine è transitabile
            # tutte le vicine (i muri)
            for x, y in coords:
                nx, ny = cx + x, cy + y
                if (nx, ny) not in visited and acc > 0:
                    visited.append((nx, ny))
                    # resetto il ciclo per fargli ricontrollare la lista intera
                    # e non farlo uscire
                    i = 0
            # Aumento l'indice per fargli scorrere la lista
            i += 1

    def perlin_builder(self, size: Tuple[int, int], octave=10, threshold=-2.0):
        from perlin_noise import PerlinNoise
        seed = randrange(1, 10000000)
        noise = PerlinNoise(octaves=octave, seed=seed)
        xpix, ypix = size
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

        if threshold != -2:
            for cy in range(xpix):
                for cx in range(ypix):
                    pic[cx][cy] = int(pic[cx][cy] >= threshold)
        return pic

    def life_builder(self, size, cicles=5, life=(2, 3), death=(1, 4, 5, 6, 7, 8), born=(3,), count=1, mask=0,
                     only_ortogonal=False):
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
                (-1, 0), (1, 0),
                (-1, 1), (0, 1), (1, 1)
            ]
            if only_ortogonal:
                coords = [
                    (0, -1),
                    (-1, 0), (1, 0),
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
