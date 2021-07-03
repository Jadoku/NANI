"""
In questo modulo sono presenti tutte le variabili globali che gestiscono tutto il
gioco, questo file può essere salvato e caricato e va caricato prima di tutti
"""

# --- Grafica --- #
from enum import Enum

mostra_tutto = False
lato_casella = 64
bordo_griglia = 2
scala_finestra = 0.5
dimensioni_finestra_iniziali = (800, 800)

# --- Pavimento --- #
mod_movimento_pietra = 1
mod_movimento_acqua = 2
mod_movimento_lava = 0

# --- Miniera --- #
livelli_miniera = 1
dimensione_lato_livello = 35
# Lista risorse [Ferro, Zolfo, Cristallo, Erbe]
risorse_per_livello = [50, 50, 50, 50]

# --- Risorse --- #
mod_movimento_risorse = 0.2

# --- Ordine di render oggetti --- #
z_pavimento = 0
z_risorse = 1
z_entita = 2
z_unita = 3


# I nomi con il doppio underscore sono necessari per
# farli ignorare nel salvataggio
# --- Lista risorse --- #
class __nomi_risorse(Enum):
    FERRO = "Ferro"
    ZOLFO = "Zolfo"
    CRISTALLO = "Cristallo"
    ERBE = "Erbe"
    SASSI = "Sassi"


def __save_data():
    import pickle
    data = {}
    for k, v in globals().copy().items():
        if "__" not in k:
            data[k] = v
    print(data)
    with open("control_panel_data.pkl", 'wb') as f:
        pickle.dump(data, f)


def __load_data():
    import pickle
    with open("control_panel_data.pkl", 'rb') as f:
        data = pickle.load(f)
        for k, v in data.items():
            globals()[k] = v
