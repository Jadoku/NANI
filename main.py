from random import choice

from Grafica import Player
from Livello import Livello
from Miniera import Miniera

# Creo la miniera
miniera = Miniera()

# Genero la miniera
miniera.genera_miniera()

# Inizializzo la grafica
gr = Player()

# Imposto il livello da visualizzare
L: Livello = miniera.livelli[0]

gr.set_map(L)
gr.start()
gr.setup()

from Nano import Minatore
from IA_base import AI_minatore

# Carica i nani in gioco con una ai
# nani = [Minatore(AI_minatore()), Guardia(AI_placeholder()), Cerusico(AI_placeholder()),Prospettore(AI_placeholder())]
nani = [Minatore(AI_minatore())]
for n in nani:
    pos = choice(L.get_accessible_cells())
    L.add_move(pos[0], pos[1], n, add=True)

for n in L.lista_nani:
    n.start()

gr.update()
