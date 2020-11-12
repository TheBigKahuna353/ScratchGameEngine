import pygame
import UI

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

class Menu:
    def __init__(self, editor, pos, names, col):
        self.editor = editor
        self.pos = pos
        self.names = names
        self.col = col
        self.font = pygame.font.Font(pygame.font.match_font('Calibri'), 14)
        self.size = self.font.render(max(self.names), True, (0, 0, 0)).get_size()
        self.text = [self.font.render(name, True, self.col['text']) for name in self.names]
    
    def draw(self):
        m_pos = self.editor.engine.m_pos
        for i, text in enumerate(self.text):
            col = self.col['bg']
            if m_pos[0] > self.pos[0] and m_pos[0] < self.pos[0] + self.size[0]:
                if m_pos[1] > self.pos[1] + i*(self.size[1]+2) and m_pos[1] < self.pos[1] + (i+1)*(self.size[1]+2):
                    col = self.col['tabs2']
                    if self.editor.engine.L_click:
                        return self.names[i]
            pygame.draw.rect(self.editor.engine.screen, col,
                (self.pos[0], self.pos[1] + i*(self.size[1] + 2), self.size[0] + 5, self.size[1] + 2))
            self.editor.engine.screen.blit(text, (self.pos[0] + 2, self.pos[1] + i*(self.size[1] + 2)))

class Panel:
    def __init__(self, editor, name, size, pos, col, border = 2):
        self.name = name
        self.size = size
        self.b = border
        self.pos = pos
        self.col_theme = col
        self.editor = editor
        self.right_click_menu = None
        self.font = pygame.font.Font(pygame.font.match_font('calibri'), 15)
        self.rect = pygame.Rect(self.pos[0] + self.b, self.pos[1] + self.b, self.size[0] - self.b*2, self.size[1] - self.b*2)
        self.name_obj = self.font.render(self.name, True, self.col_theme['text'])
        self.draw_rect()
    
    def draw_rect(self):
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.col_theme['bg'])
        pygame.draw.rect(self.surf, self.col_theme['tabs'], (self.b, self.b, self.size[0], self.size[1]))
        pygame.draw.rect(self.surf, self.col_theme['tabs2'],
            (self.b, self.b, self.name_obj.get_width() + 5, self.name_obj.get_height() + 5))
        self.surf.blit(self.name_obj, (5, 5))
    
    def draw(self):
        self.editor.engine.screen.blit(self.surf, self.pos)
    
    def stretch(self, width, pos):
        self.size[0] = width
        self.pos[0] = pos
        self.draw_rect()
    
    def __str__(self):
        return self.name
    
    def mouse_over(self):
        m_pos = self.editor.engine.m_pos
        if m_pos[0] > self.pos[0] and m_pos[0] < self.pos[0] + self.size[0]:
            return True
        return False

class Viewport:
    def __init__(self, editor):
        self.surf = editor.engine.world.surf
        self.surf.fill(colours['white'])
        self.offset = [-1000, -1000]
        self.editor = editor
        self.name = 'Scene'
        self.b = 2
        self.pos = [0, 0]
        self.size = [400, 700]
        self.col = editor.ui_color
        self.viewport = pygame.Surface([x - self.b*2 for x in self.size])
        self.static = False
        self.static_viewport = self.viewport.copy().convert()
        self.start_drag = [0, 0]
        self.start_drag_offset = []
    
    def draw(self):
        if self.static:
            self.engine.screen.blit(self.static_viewport, (self.pos[0] + self.b, self.pos[1] + self.b))
        else:
            pygame.draw.rect(self.viewport, self.col['tabs'],
                (self.pos[0] + self.b, self.pos[1] + self.b, self.size[0], self.size[1]))
            self.viewport.blit(self.surf, self.offset)
            self.editor.engine.screen.blit(self.viewport, (self.pos[0] + self.b, self.pos[1] + self.b))
        
        m_pos = self.editor.engine.m_pos
        if m_pos[0] > self.pos[0] and m_pos[0] < self.pos[0] + self.size[0]:
            # print('mouse over viewport')
            if self.editor.engine.L_click:
                if m_pos[0] > self.pos[0] and m_pos[0] < self.pos[0] + self.size[1]:
                    pos = (-self.offset[0] + m_pos[0],
                        -self.offset[1] + m_pos[1])
                    for spr in self.editor.engine.get_sprites():
                        if spr.rect().collidepoint(pos):
                            self.editor.selected_object = spr
                            break
            if self.editor.engine.R_click:
                self.start_drag = m_pos
                self.start_drag_offset = self.offset
        if self.start_drag is not None:
            if self.editor.engine.hold:
                dif = [x - y for y, x in zip(self.start_drag, m_pos)]
                self.offset = [self.start_drag_offset[i] + dif[i] for i in range(2)]
            else:
                self.start_drag = None
    
    def stretch(self, width, pos):
        self.size[0] = width
        self.viewport = pygame.Surface([x - self.b*2 for x in self.size])
        self.static_viewport = self.viewport.copy().convert()
        self.pos[0] = pos
    
    def __str__(self):
        return 'Scene'

class Inspector(Panel):
    def __init__(self, editor, size, pos, col):
        self.name = 'Inspector'
        super().__init__(editor, self.name, size, pos, col)
        self.obj = None
    
    def draw(self):
        super().draw()

        self.obj = self.editor.selected_object

        if self.obj is not None:
            o = self.font.render(self.obj.name, True, self.col_theme['text'], self.col_theme['tabs2'])
            self.editor.engine.screen.blit(o, (self.pos[0] + 15, self.pos[1] + 35))
            o = self.font.render(str(self.obj.pos), True, self.col_theme['text'], self.col_theme['tabs2'])
            self.editor.engine.screen.blit(o, (self.pos[0] + 15, self.pos[1] + 55))
            o = self.font.render(str(self.obj.size), True, self.col_theme['text'], self.col_theme['tabs2'])
            self.editor.engine.screen.blit(o, (self.pos[0] + 15, self.pos[1] + 75))


class Hierarchy(Panel):
    def __init__(self, editor, size, pos, col):
        self.name = 'Hierarchy'
        super().__init__(editor, self.name, size, pos, col)
        self.R_click_names = ['add object', 'add new window']
        self.add_obj_names = ['square']
        self.font = pygame.font.Font(pygame.font.match_font('Calibri'), 14)
    
    def draw(self):
        super().draw()
        for i, name in enumerate(self.editor.engine.sprite_names):
            obj = self.font.render(name, True, self.editor.ui_color['text'])
            self.editor.engine.screen.blit(obj, (self.pos[0] + 10, self.pos[1] + 30 + i*15))

        if self.right_click_menu is not None:
            clicked_on = self.right_click_menu.draw()
            if clicked_on is not None:
                if clicked_on == 'add new window':
                    self.editor.add_split()
                if clicked_on == 'add object':
                    pos = self.right_click_menu.pos
                    self.right_click_menu = Menu(self.editor, pos, self.add_obj_names, self.col_theme)
                    return
                if clicked_on == 'square':
                    self.editor.engine.add_object('square')
                self.right_click_menu = None

        m_pos = self.editor.engine.m_pos
        if self.mouse_over():
            if self.editor.engine.R_click:
                self.right_click_menu = Menu(self.editor, m_pos, self.R_click_names, self.col_theme)
    

        
