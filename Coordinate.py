from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Coordinate():
    def __init__(self, x=-1, y=-1):
        self.X = x
        self.Y = y

    def distanza(self,livello,bersaglio):
        """
        calcolo del percorso e della distanza pesata
        :param livello: il livello della miniera corrente
        :param bersaglio: la coordinata bersaglio
        :return: tupla(peso totale, lista coordinate percorso)
        """
        liv = livello.matrix()
        grid = Grid(matrix=liv)
        start = grid.node(self.X,self.Y)
        end = grid.node(bersaglio.X,bersaglio.Y)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        path = path[1:-1]
        path_leng = 0
        for i in path:
            x = i[0]
            y = i[1]
            path_leng += liv[x][y]
        return path_leng, path

    def __repr__(self):
        return self.X,self.Y

    def __str__(self):
        return "("+str(self.X)+", "+str(self.Y)+")"
