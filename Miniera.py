from Livello import Livello


class Miniera:
    def __init__(self, livelli: int):
        self.numero_livelli = livelli
        self.livelli = []

    def genera_miniera(self):
        """
        Genera i livelli della miniera chiamando una funzione apposita
        """
        for _ in range(self.numero_livelli):
            self.livelli.append(self._genera_livello())

    def _genera_livello(self) -> Livello:
        """
        Genera il livello che prima viene creato e poi popolato

        :return: Il livello creato
        """
        lev = Livello()
        # lev.builder(lambda: lev.perlin_builder((31, 31), threshold=0))
        lev.builder(lambda: lev.perlin_builder((31, 31)))
        return lev
