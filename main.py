import pygame
from editor import Editor
from sprite import Sprite

#constants

colours = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'light_gray': (200, 200, 200),
    'gray': (150, 150, 150),
    'dark_gray': (100, 100, 100),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0)
}

pygame.init()


class World:
    def __init__(self):
        self.size = [2000, 2000]
        self.surf = pygame.Surface(self.size)
        self.bg = colours['white']
    
    def clear(self):
        self.surf.fill(self.bg)
    
    def __repr__(self):
        return self.surf

class Engine:
    def __init__(self):
        self.fps = 0
        self.running = True
        self.world = World()
        self.m_pos = (0, 0)
        self.L_click = False
        self.R_click = False
        self.w_size = (700, 700)
        self.screen = pygame.display.set_mode(self.w_size, pygame.RESIZABLE)
        self.hold = False
        self.mouse_focus = 'window'
        self.sprites = []
        self.editor = Editor(self)
        self.clock = pygame.time.Clock()
    
    def add_object(self, type_):
        if type_ == 'square':
            surf = pygame.Surface((50, 50))
            spr = Sprite(self, 'square', [x//2 for x in self.world.size], surf)
            self.sprites.append(spr)

    def loop(self):
        while self.running:
            self.editor.update()
            for spr in self.sprites:
                spr.draw()

            self.clock.tick(self.fps)
            pygame.display.update()
            self.Events()
    
    def get_sprites(self):
        return self.sprites
    
    def Events(self):
        self.m_pos = pygame.mouse.get_pos()
        self.L_click, self.R_click = False, False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                break
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.L_click = True
                elif e.button == 3:
                    self.R_click = True
                self.hold = True
            elif e.type == pygame.MOUSEBUTTONUP:
                self.hold = False
            elif e.type == pygame.VIDEORESIZE:
                self.w_size = e.size
                self.screen = pygame.display.set_mode(e.size, pygame.RESIZABLE)
                self.editor.resize(e.w)


e = Engine()

e.loop()