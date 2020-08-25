import pygame

class Sprite:
    def __init__(self, engine, name, pos, surf):
        self.name = name
        self.pos = pos
        self.surf = surf
        self.size = surf.get_size()
        self.engine = engine
        self.col = (0, 0, 0)
    
    def draw(self):
        self.engine.world.surf.blit(self.surf, self.pos)
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
