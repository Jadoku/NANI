import pygame as pg

screen_size = larghezza, altezza = 800, 600
screen: pg.Surface
icon = {}
running = True


def start():
    global screen
    pg.init()
    screen = pg.display.set_mode(screen_size)


def setup():
    sprite_nani = {
        "minatore": (0, 1),
        "guardia": (0, 14),
        "cerusico": (3, 3),
        "prospettore": (0, 2)
    }
    tiles = {
        "pavimento": (2, 1),
        "muro": (0, 1),
        "acqua": (0, 2),
    }
    carica_immagine("immagini/sprite.png", sprite_nani)
    carica_immagine("immagini/tiles.png", tiles)


def update():
    global running
    global screen
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))
        grid(5)
        contatore = 0
        for x, y in icon.items():
            screen.blit(y, (contatore, 0))
            contatore += 65
        pg.display.update()


def carica_immagine(immagine: str, dizionario, zoom=False):
    sprites = pg.image.load(immagine).convert()
    if zoom:
        sprites = pg.transform.scale2x(sprites)
    for k, v in dizionario.items():
        rettangolo = pg.Rect(v[0] * 64, v[1] * 64, 64, 64)
        image = pg.Surface(rettangolo.size)
        image.fill((0, 0, 0, 0))
        image.blit(sprites, (0, 0), rettangolo)
        icon[k] = image


def grid(lato, dimensione=64, bordo=1):
    for x in range(lato):
        for y in range(lato):
            screen.blit(icon["pavimento"], (x*(dimensione+bordo), y*(dimensione+bordo)))
'''            pg.draw.rect(screen, (255, 255, 255),
                         [x * (dimensione + bordo), y * (dimensione + bordo), dimensione, dimensione])'''

start()
setup()
update()
