# bonamerde 2 la vendetta
import Grafica as gr
from Miniera import Miniera

miniera = Miniera(1)
miniera.genera_miniera()

L = miniera.livelli[0]
gr.mappa = L
#
# nano = Guardia(None)
# L.add_move(3,12,nano,True)
#
#
gr.start()
gr.setup()
gr.update()
