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
    test = {
        "nano1": (0, 0),
        "nano2": (2, 3)
    }
    carica_immagine("immagini/sprite.png", test)


def update():
    global running
    global screen
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        contatore = 0
        for x, y in icon.items():
            screen.blit(y, (contatore, 0))
            contatore += 64
        pg.display.update()


def carica_immagine(immagine: str, dizionario):
    sprites = pg.image.load(immagine)
    for k, v in dizionario.items():
        rettangolo = pg.Rect(v[0] * 64, v[1] * 64, 64, 64)
        image = pg.Surface(rettangolo.size)
        image.blit(sprites, (0, 0), rettangolo)
        icon[k] = image

start()
setup()
update()