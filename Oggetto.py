from abc import ABC

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


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

    def on_map_enter(self, mappa):
        self.mappa = mappa

    def distanza(self, bersaglio=None, coordinata=None):
        """
        calcolo del percorso e della distanza pesata
        :param bersaglio: la coordinata bersaglio
        :return: tupla(peso totale, lista coordinate percorso)
        """
        if bersaglio is None and coordinata is not None:
            x, y = coordinata
        else:
            x, y = bersaglio.x, bersaglio.y

        liv = self.mappa.matrix()
        grid = Grid(matrix=liv)
        start = grid.node(self.x, self.y)
        end = grid.node(x, y)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.if_at_most_one_obstacle)
        path, runs = finder.find_path(start, end, grid)
        path = path[1:-1]
        path_leng = 0
        for i in path:
            x = i[0]
            y = i[1]
            path_leng += liv[x][y]
        print(path_leng, path)
        return path_leng, path

    def rivela(self):
        self.visibile = True
