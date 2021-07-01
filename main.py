# bonamerde 2 la vendetta
from Grafica import Player
from Miniera import Miniera

miniera = Miniera(1)
miniera.genera_miniera()

L = miniera.livelli[0]
gr = Player()
gr.set_map(L)

#
# nano = Guardia(None)
# L.add_move(3,12,nano,True)
#
#
gr.start()
gr.setup()
gr.update()
