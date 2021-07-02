from Livello import Livello
import Pannello_controllo as pc


class Miniera:
    def __init__(self):
        self.numero_livelli = pc.livelli_miniera
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
        lev = Livello(pc.dimensione_lato_livello)
        lev.builder()
        return lev
