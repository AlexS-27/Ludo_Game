import pygame

# cell type
NORMAL_HORIZONTAL = "normal_horizontal"
NORMAL_VERTICAL = "normal_vertical"
HOME_AREA = "home_area"
STORAGE = "storage"

# Coulors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# class to create the cells
class Cell:
    def __init__(self, row, col, width, height, cell_type= NORMAL_HORIZONTAL, id=None, color=WHITE):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cell_type = cell_type
        self.id = id
        self.basic = WHITE
        self.color = color
        self.border_width = 1

    def draw(self, surface):
        x = self.col * self.width
        y = self.row * self.height

        if self.cell_type == STORAGE:
            # cercle
            center = (x + self.width//2, y + self.height//2)
            radius = min(self.width, self.height)//2 - 4
            pygame.draw.circle(surface, self.color, center, radius)
            pygame.draw.circle(surface, BLACK, center, radius, 2)
        else:
            # rectangle
            pygame.draw.rect(surface, self.color, (x, y, self.width, self.height))

            if self.border_width > 0:
                pygame.draw.rect(surface, BLACK, (x, y, self.width, self.height), 1)

        # Afficher l'ID si case jouable
        if self.id is not None and self.cell_type in [NORMAL_HORIZONTAL, NORMAL_VERTICAL]:
            font = pygame.font.SysFont("Arial", 16)
            text = font.render(str(self.id), True, BLACK)
            surface.blit(text, (x + 10, y + 10))