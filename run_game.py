import pygame
from threading import Thread

def run(engine):
    Thread(target=start, args=(engine,)).start()

def start(engine):
    pygame.init()

    screen2 = pygame.display.set_mode((500, 500))

    while True:
        pass