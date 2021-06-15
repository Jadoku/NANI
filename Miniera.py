from Livello import Livello


class Miniera:
    def __init__(self, livelli: int):
        self.numero_livelli = livelli

        self.livelli = []

    def genera_miniera(self):
        for _ in range(self.numero_livelli):
            self.livelli.append(self._genera_livello())

    def _genera_livello(self) -> Livello:
        return self.generatore_livello(Livello())

    def generatore_livello(self, livello: Livello) -> Livello:
        return livello
