import pygame

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()

#setup window's title
pygame.display.set_caption("Ludo Game")

# Grid
ROWS, COLS = 15, 15
CELL_WIDTH = 50
CELL_HEIGHT = 50

# cell type
NORMAL_HORIZONTAL = "normal_horizontal"
NORMAL_VERTICAL = "normal_vertical"
HOME_AREA = "home_area"
STORAGE = "storage"
SAFE_PATH = "safe_path"
CENTER = "center"


# Coulors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#Alex
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
        if self.id is not None and self.cell_type not in [HOME_AREA, STORAGE]:
            font = pygame.font.SysFont("Arial", 16)
            text = font.render(str(self.id), True, BLACK)
            surface.blit(text, (x + 10, y + 10))


# Créer la
# Avec l'aide de chatGPT -Alex
def draw_wide_arrow(surface, start_row, start_col, base_width=3, end_row=None, end_col=None, color=RED, cell_width=40, cell_height = 40,  direction="down"):
    """
    Dessine une flèche large :
    - base_width : nombre de cases pour la base
    - start_row, start_col : case de départ (coin supérieur/gauche de la base)
    - end_row, end_col : case d'arrivée (pointe)
    - direction : "down", "up", "left", "right"
    """
    if end_row is None:
        end_row = start_row + 1
    if end_col is None:
        end_col = start_col

    # Coordonnées de départ (en pixels)
    x_start = start_col * cell_width
    y_start = start_row * cell_height

    # Coordonnées de la pointe (centre de la case d’arrivée)
    x_end = end_col * cell_width+ cell_width // 2
    y_end = end_row * cell_height + cell_height // 2

    if direction == "down":
        # base horizontale sur la ligne start_row
        x1 = x_start
        y1 = y_start
        x2 = x_start + base_width * cell_width
        y2 = y_start
    elif direction == "up":
        x1 = x_start
        y1 = y_start + cell_height
        x2 = x_start + base_width * cell_width
        y2 = y_start + cell_height
    elif direction == "right":
        x1 = x_start
        y1 = y_start
        x2 = x_start
        y2 = y_start + base_width * cell_height
    elif direction == "left":
        x1 = x_start + cell_width
        y1 = y_start
        x2 = x_start + cell_width
        y2 = y_start + base_width * cell_height

    points = [(x1, y1), (x2, y2), (x_end, y_end)]
    pygame.draw.polygon(surface, color, points)


#create the grid + id
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
for r in range(1, 6):
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
for c in range(13, 8, -1):
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
for r in range(13, 8, -1):
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

# Chemin horizontal rouge
for c in range(1, 6):
    grid[6][c].cell_type = NORMAL_HORIZONTAL
    grid[6][c].id = game_id_counter
    game_id_counter += 1

# Chemin vertical rouge
for r in range(5, 0, -1):
    grid[r][6].cell_type = NORMAL_VERTICAL
    grid[r][6].id = game_id_counter
    game_id_counter += 1

# Rouge (monte vers le centre)
safe_id = 200
for r in range(1, 6):
    grid[r][7].cell_type = SAFE_PATH
    grid[r][7].id = safe_id
    safe_id += 1

# Jaune (descend vers le centre)
safe_id = 300
for r in range(9, 14):
    grid[r][7].cell_type = SAFE_PATH
    grid[r][7].id = safe_id
    safe_id += 1

# Vert (va vers la droite)
safe_id = 400
for c in range(1, 6):
    grid[7][c].cell_type = SAFE_PATH
    grid[7][c].id = safe_id
    safe_id += 1

# Bleu (va vers la gauche)
safe_id = 500
for c in range(9, 14):
    grid[7][c].cell_type = SAFE_PATH
    grid[7][c].id = safe_id
    safe_id += 1



#Alex
#Create the different cell with colors
def color_ludo():
    #Red zone
    for r in range(0,6):
        for c in range(0,6):
            grid[r][c].color = RED
            grid[r][c].border_width = 0
    #Blue zone
    for r in range(0,6):
        for c in range(9,15):
            grid[r][c].color = BLUE
            grid[r][c].border_width = 0
    #Yellow zone
    for r in range(9,15):
        for c in range(9,15):
            grid[r][c].color = YELLOW
            grid[r][c].border_width = 0
    #Green zone
    for r in range(9,15):
        for c in range(0,6):
            grid[r][c].color = GREEN
            grid[r][c].border_width = 0
    #Red safe zone
    for r in range(1,6):
        c = 7
        grid[r][c].color = RED
    #Yellow safe zone
    for r in range(9,14):
        c=7
        grid[r][c].color = YELLOW
    #Green safe zone
    for c in range(1,6):
        r= 7
        grid[r][c].color = GREEN
    #Blue safe zone
    for c in range(9,14):
        r= 7
        grid[r][c].color = BLUE
    #Red entry
    for r in range(1,2):
        c=6
        grid[r][c].color = RED
    #Yellow entry
    for r in range(13,14):
        c=8
        grid[r][c].color = YELLOW
    #Green entry
    for c in range(1,2):
        r=8
        grid[r][c].color = GREEN
    #Blue entry
    for c in range(13,14):
        r= 6
        grid[r][c].color = BLUE


color_ludo()
#laod image

run = True
#main loop
while run:

    events = pygame.event.get()
    for event in events:

        #quit pygame
        if event.type == pygame.QUIT:
            run = False
        #React to resize
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        #Cliquer : Montre l'id de la case -Alex
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // CELL_WIDTH
            row = my // CELL_HEIGHT
            clicked_cell = grid[row][col]
            print(f"Case cliquée: ID={clicked_cell.id}, Type={clicked_cell.cell_type}")

    screen.fill((0,0,0))

    # draw all cells -Alex
    for row in grid:
        for cell in row:
            cell.draw(screen)

    #Draw arrow
    #Red arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3, end_row=7, end_col=7, color=RED, cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="down")
    #Green arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3, end_row=7, end_col=7, color=GREEN, cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="right")
    #Yellow arrow
    draw_wide_arrow(screen, start_row=8, start_col=6, base_width=3, end_row=7, end_col=7, color=YELLOW, cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="up")
    #Blue arrow
    draw_wide_arrow(screen, start_row=6, start_col=8, base_width=3, end_row=7, end_col=7, color=BLUE, cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="left")

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
