from abc import ABC
from enum import Enum
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Oggetto(ABC):
    def __init__(self):
        self.x=-1
        self.y=-1
        self.mod_movimento=0
        self.priorita = 0
        self.nome = ""
        self.mappa = None

    def distanza(self,livello,bersaglio):
        """
        calcolo del percorso e della distanza pesata
        :param livello: il livello della miniera corrente
        :param bersaglio: la coordinata bersaglio
        :return: tupla(peso totale, lista coordinate percorso)
        """
        liv = livello.matrix()
        grid = Grid(matrix=liv)
        start = grid.node(self.x,self.y)
        end = grid.node(bersaglio.x,bersaglio.y)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.if_at_most_one_obstacle)
        path, runs = finder.find_path(start, end, grid)
        path = path[1:-1]
        path_leng = 0
        for i in path:
            x = i[0]
            y = i[1]
            path_leng += liv[x][y]
        return path_leng, path
