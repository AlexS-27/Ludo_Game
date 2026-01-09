import pygame

# cell type
NORMAL_HORIZONTAL = "normal_horizontal"
NORMAL_VERTICAL = "normal_vertical"
HOME_AREA = "home_area"
STORAGE = "storage"
SAFE_PATH = "safe_path"   # <- ajouté pour centraliser la constante
CENTER = "center"        # <- optionnel, utile si besoin futur

# Colors
RED = (230, 60, 60)
GREEN = (60, 200, 100)
BLUE = (70, 130, 255)
WHITE = (245, 245, 245)
YELLOW = (240, 220, 90)
BLACK = (10, 10, 10)
BORDER = (40, 40, 48)

# class to create the cells
class Cell:
    def __init__(self, row, col, width, height, cell_type=NORMAL_HORIZONTAL, id=None, color=WHITE):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cell_type = cell_type
        self.id = id
        self.basic = WHITE
        self.color = color
        self.border_width = 1

    def draw(self, surface,  x_offset=0, y_offset=0):
        x = x_offset + self.col * self.width
        y = y_offset + self.row * self.height

        rect = pygame.Rect(x, y, self.width, self.height)
        border_radius = 8

        # draw shadow for home area and playable cells
        shadow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 55), shadow.get_rect(), border_radius=border_radius)
        surface.blit(shadow, (x + 3, y + 3))

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