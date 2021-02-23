from Entita import Entita
from Oggetto import Cat

class Livello():
    def __init__(self, lato: int = 31):
        # self.matrix=[[[0,0,0]]*lato for _ in range(lato)]
        self.lista_oggetti = []
        self.lato = lato

    def matrix(self,phase=False):
        """
        popola la matrice con blocchi e pesi. se l'unità ignora i muri passa phase=True
        :return: matrice con blocchi o pesi
        """
        matrix=[]
        for i in range(self.lato):
            r = []
            for j in range(self.lato):
                if phase:
                    r.append(1)
                else:
                    r.append(self.is_accessible(i,j))
            matrix.append(r)
        return matrix

    def get_coord(self, x, y, z: Cat = None):
        if z is None:
            return list(filter(lambda n: n.x == x and n.y == y, self.lista_oggetti)).sort(key=lambda n: n.categoria, reverse=False)
        else:
            return list(filter(lambda n: n.x == x and n.y == y and n.categoria == z, self.lista_oggetti))

    def is_accessible(self, x, y):
        """
        controlla se una casella è bloccante
        :param x: coordinata X
        :param y: coordinata Y
        :return: 0 se bloccante, altrimenti modificatore di movimento.
        """
        k = 0
        for i in self.get_coord(x,y):
            if i.block:
                return 0
            else:
                k += i.mod_movimento
        return max(k,0)

    def add_move(self,x,y,oggetto,add:bool=False,phase:bool=False):
        """
        aggiunge o muove un oggetto all'interno della griglia
        :param x: destinazione x
        :param y: destinazione y
        :param oggetto: oggetto da muovere o aggiungere
        :param add: se true, aggiunge un oggetto non presente sulla griglia
        :param phase: ignora se il terreno è bloccante o meno
        :return: true se è possibile, false se non è possibile
        """
        if self.check_bounds(x,y) and (bool(self.is_accessible(x,y)) or phase):
            oggetto.x = x
            oggetto.y = y
            if add:
                self.lista_oggetti.append(oggetto)
            return True
        else:
            print("non puoi aggiungere/muovere un oggetto in una casella occupata")
            return False

    def remove_item(self,oggetto):
        self.lista_oggetti.remove(oggetto)
        if isinstance(oggetto,Entita):
            for i in oggetto.risorsa:
                self.add_move(oggetto.x,oggetto.y,i,True)
        return oggetto

    def check_bounds(self,x,y):
        return 0<=x<self.lato and 0<=y<self.lato
