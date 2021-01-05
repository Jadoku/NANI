class Livello():
    def __init__(self, lato: int = 21):
        # self.matrix=[[[0,0,0]]*lato for _ in range(lato)]
        self.lista_oggetti = []

    def get_coord(self, x, y, z = None):
        if z is None:
            return list(filter(lambda n: n.x == x and n.y == y, self.lista_oggetti)).sort(key=lambda n: n.z,reverse=False)
        else:
            return list(filter(lambda n: n.x == x and n.y == y and n.z == z, self.lista_oggetti))

    def is_empty(self, x, y, z):
        if not self.get_coord(x, y, z):
            return True
        else:
            return False

    def add_item(self,x,y,oggetto):
        if oggetto.z == 1 or self.is_empty(x,y,oggetto.z):
            oggetto.x = x
            oggetto.y = y
            self.lista_oggetti.append(oggetto)
            return True
        else:
            print("non puoi aggiungere un oggetto in una casella occupata")
            return False

    def remove_item(self,oggetto):
        self.lista_oggetti.remove(oggetto)
        return oggetto

    def move_item(self,oggetto,x,y):
        if oggetto.z != 1:
            if self.is_empty(x,y,oggetto.z):
                return True
            else:
                return False
        else:
            return True
