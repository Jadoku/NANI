from typing import List

import pygame as pg

from Livello import Livello
from Oggetto import Oggetto

mappa: Livello
latocasella = 64
bordo = 2
lato_miniera = 31
dim_miniera = (latocasella+bordo)*lato_miniera-bordo
screen_size = larghezza, altezza = dim_miniera//2, dim_miniera//2
screen: pg.Surface
main_screen: pg.Surface = pg.Surface((dim_miniera, dim_miniera), flags=pg.SRCALPHA)
icon = {}
running = True

def start():
    global screen
    pg.init()
    screen = pg.display.set_mode(screen_size,pg.RESIZABLE)


def setup():
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
    }
    carica_immagine("immagini/spriteFix.png", sprite_nani)
    carica_immagine("immagini/tiles.png", tiles)


def update():
    global running
    global screen
    global main_screen
    while running:

        # --- GESTIONE EVENTI ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                old_surface_saved = screen
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                screen.blit(old_surface_saved, (0, 0))
                del old_surface_saved
            if event.type == pg.KEYDOWN:
                omino = mappa.lista_oggetti[0]
                if event.key == pg.K_DOWN:
                    mappa.add_move(omino.x,omino.y+1,omino)
                if event.key == pg.K_UP:
                    mappa.add_move(omino.x,omino.y-1,omino)
                if event.key == pg.K_RIGHT:
                    mappa.add_move(omino.x+1,omino.y,omino)
                if event.key == pg.K_LEFT:
                    mappa.add_move(omino.x-1,omino.y,omino)
        # --- FINE GESTIONE EVENTI ---

        screen.fill(pg.Color("black"))
        grid(lato_miniera, latocasella, bordo)

        oggetti: List[Oggetto] = mappa.lista_oggetti.copy()
        for x in oggetti:
            main_screen.blit(icon[x.sprite], (x.x * (latocasella+bordo), x.y * (latocasella+bordo)))

        #pg.transform.scale(main_screen, (main_screen.get_width()//2, main_screen.get_height()//2), main_screen)
        main_screen2 = pg.transform.rotozoom(main_screen,0,0.5)
        screen.blit(main_screen2,(0,0))
        pg.display.update()


def carica_immagine(immagine: str, dizionario, zoom=False):
    sprites = pg.image.load(immagine).convert_alpha()
    if zoom:
        sprites = pg.transform.scale2x(sprites)
    for k, v in dizionario.items():
        rettangolo = pg.Rect(v[0] * 64, v[1] * 64, 64, 64)
        image = pg.Surface(rettangolo.size, flags=pg.SRCALPHA)
        image.blit(sprites, (0, 0), rettangolo)
        icon[k] = image


def grid(lato, dimensione, spessore_bordo=0):
    for x in range(lato):
        for y in range(lato):
            main_screen.blit(icon["pavimento"], (x * (dimensione + spessore_bordo), y * (dimensione + spessore_bordo)))
