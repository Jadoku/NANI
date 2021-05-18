# bonamerde 2 la vendetta
from Livello import *
import Grafica as gr
from Nano import *

L = Livello()
gr.mappa = L

nano = Guardia(None)
L.add_move(3,12,nano,True)


gr.start()
gr.setup()
gr.update()
