from abc import ABC

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder


class Oggetto(ABC):
    def __init__(self):
        self.x = -1
        self.y = -1
        self.z = 0
        self.mod_movimento = 0
        self.priorita = 0
        self.nome = ""
        self.mappa = None
        self.sprite = None
        self.visibile = False
        self.__finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)

    def on_map_enter(self, mappa):
        self.mappa = mappa

    def distanza(self, bersaglio=None):
        """
        calcolo del percorso e della distanza pesata
        :param bersaglio: la coordinata bersaglio
        :return: tupla(peso totale, lista coordinate percorso, distanza non modificata dal taglio dell'ultima casella)
        """
        x, y = bersaglio.x, bersaglio.y
        liv = self.mappa.matrix()
        grid = Grid(matrix=liv)
        start = grid.node(self.x, self.y)
        end = grid.node(x, y)
        path, runs = self.__finder.find_path(start, end, grid)
        print("partenza", (self.x, self.y), "arrivo", (x, y), path, runs)
        if not path:
            return 0, path, -1
        path.remove((self.x, self.y)) # rimuovo la posizione del giocatore
        if (self.x, self.y) != (x, y):
            distanza_reale = len(path)  # Ho la distanza dal personaggio in quadretti
            path.remove((x, y))  # tolgo le coordinate del bersaglio
        else:
            distanza_reale = 0  # se il bersaglio nella stessa casella restituisce zero
        path_leng = 0
        grid.cleanup()
        for x, y in path:
            path_leng += liv[x][y]
        return path_leng, path, distanza_reale

    def rivela(self):
        self.visibile = True
