from typing import List

import pygame as pg

import Pannello_controllo as pc
from Livello import Livello
from Oggetto import Oggetto


class Player:
    def __init__(self):
        self.latocasella = pc.lato_casella
        self.bordo = pc.bordo_griglia
        self.mostra_tutto = pc.mostra_tutto
        self.resize_scale = pc.scala_finestra
        self.dimensioni_iniziali = pc.dimensioni_finestra_iniziali
        self.icon = {}
        self.running = True

    def set_map(self, livello: Livello):
        self.mappa: Livello = livello
        self.dim_miniera = (self.latocasella + self.bordo) * self.mappa.lato - self.bordo
        self.screen_size = self.larghezza, self.altezza = self.dimensioni_iniziali[0], self.dimensioni_iniziali[1]
        self.screen: pg.Surface
        self.main_screen: pg.Surface = pg.Surface((self.dim_miniera, self.dim_miniera), flags=pg.SRCALPHA)

    def start(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size, pg.RESIZABLE)

    def setup(self):
        sprite_nani = {
            "minatore": (0, 1),
            "guardia": (0, 14),
            "cerusico": (3, 3),
            "prospettore": (0, 2)
        }
        tiles = {
            "vuoto": (0, 0),
            "pavimento": (3, 1),
            "muro": (0, 1),
            "acqua": (0, 2),
            "lava": (3, 2)
        }
        icone_risorse = {
            "ferro": (1, 1),
            "zolfo": (0, 1),
            "cristallo": (0, 0),
            "erbe": (1, 0)
        }
        forzieri = {
            "forziere": (0, 2)
        }
        self.carica_immagine("immagini/spriteFix.png", sprite_nani)
        self.carica_immagine("immagini/tiles.png", tiles)
        self.carica_immagine("immagini/gemme2.png", icone_risorse)
        self.carica_immagine("immagini/treasure_chests_32x32.png", forzieri)
        self.carica_immagine("immagini/sassi.png", {"sassi":(0, 0)})


    def update(self):
        while self.running:
            # --- GESTIONE EVENTI ---
            for event in pg.event.get():
                self.__gestione_quit(event)
                self.__gestione_resize_window(event)
                self.__gestione_input(event)
            # --- FINE GESTIONE EVENTI ---

            self.__render_griglia()
            self.__render_oggetti()
            self.__render_ui()
            self.__gestione_update()

    def __gestione_quit(self, event):
        if event.type == pg.QUIT:
            self.running = False

    def __gestione_resize_window(self, event):
        if event.type == pg.VIDEORESIZE:
            old_surface_saved = self.screen
            less = min(event.w, event.h)
            self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self.resize_scale = less/self.dim_miniera
            self.screen.blit(old_surface_saved, (0, 0))
            del old_surface_saved

    def __gestione_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F5:
                self.mostra_tutto = not self.mostra_tutto
                pass

    def __render_griglia(self):
        self.screen.fill(pg.Color("black"))
        self.grid(self.mappa.lato, self.latocasella, self.bordo)

    def __render_oggetti(self):
        oggetti: List[Oggetto] = self.mappa.lista_oggetti_render.copy()
        for x in oggetti:
            if x.visibile or self.mostra_tutto:
                self.main_screen.blit(self.icon[x.sprite],
                                      (x.x * (self.latocasella + self.bordo), x.y * (self.latocasella + self.bordo)))

    def __render_ui(self):
        pass

    def __gestione_update(self):
        main_screen2 = pg.transform.rotozoom(self.main_screen, 0, self.resize_scale)
        self.screen.blit(main_screen2, (0, 0))
        pg.display.update()

    def carica_immagine(self, immagine: str, dizionario, zoom=False):
        sprites = pg.image.load(immagine).convert_alpha()
        if zoom:
            sprites = pg.transform.scale2x(sprites)
        for k, v in dizionario.items():
            rettangolo = pg.Rect(v[0] * 64, v[1] * 64, 64, 64)
            image = pg.Surface(rettangolo.size, flags=pg.SRCALPHA)
            image.blit(sprites, (0, 0), rettangolo)
            self.icon[k] = image

    def grid(self, lato, dimensione, spessore_bordo=0):
        for x in range(lato):
            for y in range(lato):
                self.main_screen.blit(self.icon["vuoto"],
                                      (x * (dimensione + spessore_bordo), y * (dimensione + spessore_bordo)))
