import pygame

class Cell:
    def __init__(self, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.color = (0, 0, 0)
        self.border_width = 1
        self.id = None
        self.cell_type = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (self.col * self.width, self.row * self.height, self.width, self.height))
        if self.border_width:
            pygame.draw.rect(surface, (0, 0, 0),
                             (self.col * self.width, self.row * self.height, self.width, self.height), self.border_width)
