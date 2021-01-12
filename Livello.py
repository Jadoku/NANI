from Entita import Entita
from Oggetto import Cat

class Livello():
    def __init__(self, lato: int = 21):
        # self.matrix=[[[0,0,0]]*lato for _ in range(lato)]
        self.lista_oggetti = []

    def get_coord(self, x, y, z: Cat = None):
        if z is None:
            return list(filter(lambda n: n.x == x and n.y == y, self.lista_oggetti)).sort(key=lambda n: n.categoria, reverse=False)
        else:
            return list(filter(lambda n: n.x == x and n.y == y and n.categoria == z, self.lista_oggetti))

    def is_accessible(self, x, y): #se terreno bloccante risultato = 0, altrimenti risultato = modificatore del movimento
        k = 0
        for i in self.get_coord(x,y):
            if i.block:
                return 0
            else:
                k += i.mod_movimento
        return k

    def add_move(self,x,y,oggetto,add:bool=False,phase:bool=False):
        if bool(self.is_accessible(x,y)) or phase:
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


