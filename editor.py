import pygame
from panels import *

class Ui_button:
    def __init__(self, x, y, w, h, col_theme, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.col = col_theme
    
    def update(self):
        pass

class Split:
    def __init__(self, editor, panel1, panel2):
        self.panel1 = panel1
        self.panel2 = panel2
        self.split_dir = 'vertical'
        self.pos = panel1.pos
        self.split_location = panel2.pos[0] - self.pos[0]
        self.size = [self.panel1.size[0] + self.panel2.size[0], panel1.size[0]]
        self.editor = editor
        self.adjusting = False
    
    def draw(self):
        self.panel1.draw()
        self.panel2.draw()
        m_pos = self.editor.engine.m_pos
        if m_pos[0] > self.split_location - 4 + self.pos[0] and m_pos[0] < self.split_location + 4 + self.pos[0]:
            if self.editor.engine.L_click:
                self.adjusting = True
        if self.adjusting:
            self.move_center(m_pos[0] - self.pos[0])
            if not self.editor.engine.hold:
                self.adjusting = False
    
    def stretch(self, width, pos):
        self.size[0] = width
        self.pos[0] = pos
        self.split_location = width//2
        self.panel1.stretch(width//2, pos)
        self.panel2.stretch(width//2, pos + self.split_location)
    
    def move_center(self, pos):
        if pos > self.size[0] or pos < 0:
            return
        self.panel1.stretch(pos, self.pos[0])
        self.panel2.stretch(self.size[0] - pos, self.pos[0] + pos)
        self.split_location = pos
    
    def get_panel(self, m_pos):
        if m_pos[0] > self.pos[0] + self.split_location:
            if isinstance(self.panel2, Split):
                return self.panel2.get_panel(m_pos)
            self.side = 2
            return self, self.panel2
        if isinstance(self.panel1, Split):
            return self.panel1.get_panel(m_pos)
        self.side = 1
        return self, self.panel1
    
    def set_panel_split(self, split):
        if self.side == 1:
            self.panel1 = split
        else:
            self.panel2 = split
    
    def __str__(self):
        return 'Split: ' + str(self.panel1) + ', ' + str(self.panel2)

class Editor:
    def __init__(self, engine):
        self.selected_object = None
        self.engine = engine
        self.ui_color =  {
            'bg': colours['dark_gray'],
            'text': colours['white'],
            'tabs': colours['gray'],
            'tabs2': colours['light_gray']
            }
        mid_split = Split(self, Inspector(self, [100, 700], [400, 0], self.ui_color),
            Hierarchy(self, [200, 700], [500, 0], self.ui_color))
        self.panels = Split(self, Viewport(self), mid_split)

    def resize(self, size):
        self.panels.stretch(size, 0)

    def update(self):
        #reset self.engine.screen
        self.engine.screen.fill(self.ui_color['bg'])
        #draw tabs
        self.panels.draw()


        pygame.display.update()
    
    def add_split(self):
        old_split, old_panel = self.panels.get_panel(self.engine.m_pos)
        print(self.panels)
        new_pos = [old_panel.pos[0] + old_panel.size[0]//2, old_panel.pos[1]]
        new_size = [old_panel.size[0]//2, old_panel.size[1]]
        new_panel_r = Panel(self, 'New Panel', new_size, new_pos, self.ui_color)
        old_panel.stretch(new_size[0], old_panel.pos[0])
        new_split = Split(self, old_panel, new_panel_r)
        old_split.set_panel_split(new_split)
        print(self.panels)