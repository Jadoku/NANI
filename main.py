from Grafica import Player
from Miniera import Miniera
import Pannello_controllo as pc


# Creo la miniera
miniera = Miniera()

# Genero la miniera
miniera.genera_miniera()

# Inizializzo la grafica
gr = Player()

# Imposto il livello da visualizzare


L = miniera.livelli[0]
gr.mostra_tutto = False
gr.set_map(L)
gr.start()
gr.setup()
gr.update()
