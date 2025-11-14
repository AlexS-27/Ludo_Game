import pygame

pygame.init()

# Setup pygame
screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
pygame.display.set_caption("Ludo Game")

# Grille
ROWS, COLS = 15, 15
CELL_WIDTH = 80
CELL_HEIGHT = 40

# Types de cases
NORMAL_HORIZONTAL = "normal_horizontal"
NORMAL_VERTICAL = "normal_vertical"
HOME_AREA = "home_area"
STORAGE = "storage"

# Couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classe Cell
class Cell:
    def __init__(self, row, col, width, height, cell_type= NORMAL_HORIZONTAL, id=None, color=WHITE):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cell_type = cell_type
        self.id = id
        self.color = color

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
            pygame.draw.rect(surface, BLACK, (x, y, self.width, self.height), 1)

        # Afficher l'ID si case jouable
        if self.id is not None and self.cell_type in [NORMAL_HORIZONTAL, NORMAL_VERTICAL]:
            font = pygame.font.SysFont("Arial", 16)
            text = font.render(str(self.id), True, BLACK)
            surface.blit(text, (x + 10, y + 10))

# Créer la grille
grid = []
for r in range(ROWS):
    grid.append([])
    for c in range(COLS):
        grid[r].append(Cell(r, c, CELL_WIDTH, CELL_HEIGHT))

# Zones home_area
home_areas = {
    "RED": (0, 0),
    "BLUE": (0, 9),
    "YELLOW": (9, 9),
    "GREEN": (9, 0)
}
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}

for color_name, (base_r, base_c) in home_areas.items():
    for r in range(base_r, base_r + 6):
        for c in range(base_c, base_c + 6):
            grid[r][c].cell_type = HOME_AREA
            grid[r][c].color = colors[color_name]

# Cases de stockage dans home_area (4 par zone)
storage_offsets = [(1,1), (1,4), (4,1), (4,4)]
storage_id_counter = 100
for color_name, (base_r, base_c) in home_areas.items():
    for dr, dc in storage_offsets:
        r = base_r + dr
        c = base_c + dc
        grid[r][c].cell_type = STORAGE
        grid[r][c].id = storage_id_counter
        grid[r][c].color = WHITE
        storage_id_counter += 1

# Chemin jouable (indexation 1 → 56)
game_id_counter = 1

# Chemin horizontal en haut
for c in range(6, 9):
    grid[0][c].cell_type = NORMAL_HORIZONTAL
    grid[0][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical bleu
for r in range(1, 7):
    grid[r][8].cell_type = NORMAL_VERTICAL
    grid[r][8].id = game_id_counter
    game_id_counter += 1

# Chemin horizontal bleu
for c in range(9, 15):
    grid[6][c].cell_type = NORMAL_HORIZONTAL
    grid[6][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical droite
for r in range(7, 9):
    grid[r][14].cell_type = NORMAL_VERTICAL
    grid[r][14].id = game_id_counter
    game_id_counter += 1

# Chemin horizontal jaune
for c in range(13, 7, -1):
    grid[8][c].cell_type = NORMAL_HORIZONTAL
    grid[8][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical jaune
for r in range(9, 14):
    grid[r][8].cell_type = NORMAL_VERTICAL
    grid[r][8].id = game_id_counter
    game_id_counter += 1

# Chemin horizontal bas
for c in range(8, 5, -1):
    grid[14][c].cell_type = NORMAL_HORIZONTAL
    grid[14][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical vert
for r in range(13, 7, -1):
    grid[r][6].cell_type = NORMAL_VERTICAL
    grid[r][6].id = game_id_counter
    game_id_counter += 1

# Chemin horizontal vert
for c in range(5, 0, -1):
    grid[8][c].cell_type = NORMAL_HORIZONTAL
    grid[8][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical gauche
for r in range(8, 5, -1):
    grid[r][0].cell_type = NORMAL_VERTICAL
    grid[r][0].id = game_id_counter
    game_id_counter += 1

# Chemin horizontal vert
for c in range(1, 6):
    grid[6][c].cell_type = NORMAL_HORIZONTAL
    grid[6][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical bleu
for r in range(6, 0, -1):
    grid[r][6].cell_type = NORMAL_VERTICAL
    grid[r][6].id = game_id_counter
    game_id_counter += 1

# 4️⃣ Boucle principale
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // CELL_WIDTH
            row = my // CELL_HEIGHT
            clicked_cell = grid[row][col]
            print(f"Case cliquée: ID={clicked_cell.id}, Type={clicked_cell.cell_type}")

    screen.fill((0,0,0))

    for row in grid:
        for cell in row:
            cell.draw(screen)

    pygame.display.flip()

pygame.quit()
