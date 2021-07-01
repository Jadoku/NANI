from typing import List

import pygame as pg

from Livello import Livello
from Oggetto import Oggetto


class Player:
    def __init__(self):
        self.latocasella = 64
        self.bordo = 2
        self.mostra_tutto = False
        self.icon = {}
        self.running = True

    def set_map(self, livello: Livello):
        self.mappa: Livello = livello
        self.dim_miniera = (self.latocasella + self.bordo) * self.mappa.lato - self.bordo
        self.screen_size = self.larghezza, self.altezza = self.dim_miniera // 2, self.dim_miniera // 2
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

    def update(self):
        while self.running:

            # --- GESTIONE EVENTI ---
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.VIDEORESIZE:
                    old_surface_saved = self.screen
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    self.screen.blit(old_surface_saved, (0, 0))
                    del old_surface_saved
                if event.type == pg.KEYDOWN:
                    omino = self.mappa.lista_oggetti[0]
                    if event.key == pg.K_DOWN:
                        self.mappa.add_move(omino.x, omino.y + 1, omino)
                    if event.key == pg.K_UP:
                        self.mappa.add_move(omino.x, omino.y - 1, omino)
                    if event.key == pg.K_RIGHT:
                        self.mappa.add_move(omino.x + 1, omino.y, omino)
                    if event.key == pg.K_LEFT:
                        self.mappa.add_move(omino.x - 1, omino.y, omino)
            # --- FINE GESTIONE EVENTI ---

            self.screen.fill(pg.Color("black"))
            self.grid(self.mappa.lato, self.latocasella, self.bordo)

            oggetti: List[Oggetto] = self.mappa.lista_oggetti.copy()
            for x in oggetti:
                if x.visibile or self.mostra_tutto:
                    self.main_screen.blit(self.icon[x.sprite],
                                      (x.x * (self.latocasella + self.bordo), x.y * (self.latocasella + self.bordo)))

            # pg.transform.scale(main_screen, (main_screen.get_width()//2, main_screen.get_height()//2), main_screen)
            main_screen2 = pg.transform.rotozoom(self.main_screen, 0, 0.5)
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
                self.main_screen.blit(self.icon["pavimento"],
                                      (x * (dimensione + spessore_bordo), y * (dimensione + spessore_bordo)))
