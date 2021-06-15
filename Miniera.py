from Livello import Livello

class Miniera:
    def __init__(self, livelli: int):
        self.numero_livelli = livelli

        self.livelli = []

    def genera_miniera(self):
        for l in range(self.numero_livelli):
            self.livelli.append(self._genera_livello())

    def _genera_livello(self) -> Livello:
        pass
