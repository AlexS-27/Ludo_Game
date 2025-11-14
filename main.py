import pygame

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()

#setup window's title
pygame.display.set_caption("Ludo Game")

# define game variable
ROWS, COLS = 15, 15
CELL_WIDTH = 80
CELL_HEIGHT = 40

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#Alex
# class to create the cells
class Cell:
    def __init__(self, row, col, width, height, id):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.id = id
        self.color = WHITE
        self.border_width = 1

    def draw(self, surface):
        x = self.col * self.width
        y = self.row * self.height

        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height))

        if self.border_width > 0:
            pygame.draw.rect(surface, BLACK, (x, y, self.width, self.height), 1)

# Avec l'aide de chatGPT -Alex
def draw_wide_arrow(surface, start_row, start_col, base_width=3, end_row=None, end_col=None, color=RED, cell_size=40, direction="down"):
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
    x_start = start_col * cell_size
    y_start = start_row * cell_size

    # Coordonnées de la pointe (centre de la case d’arrivée)
    x_end = end_col * cell_size + cell_size // 2
    y_end = end_row * cell_size + cell_size // 2

    if direction == "down":
        # base horizontale sur la ligne start_row
        x1 = x_start
        y1 = y_start
        x2 = x_start + base_width * cell_size
        y2 = y_start
    elif direction == "up":
        x1 = x_start
        y1 = y_start + cell_size
        x2 = x_start + base_width * cell_size
        y2 = y_start + cell_size
    elif direction == "right":
        x1 = x_start
        y1 = y_start
        x2 = x_start
        y2 = y_start + base_width * cell_size
    elif direction == "left":
        x1 = x_start + cell_size
        y1 = y_start
        x2 = x_start + cell_size
        y2 = y_start + base_width * cell_size

    points = [(x1, y1), (x2, y2), (x_end, y_end)]
    pygame.draw.polygon(surface, color, points)


#create the grid + id
grid = []
id_counter = 0

for row in range(ROWS):
    grid.append([])
    for col in range(COLS):
        grid[row].append(Cell(row, col, CELL_WIDTH, CELL_HEIGHT, id_counter))
        id_counter += 1

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

            if 0 <= row < ROWS and 0 <= col < COLS:
                print("Case cliqué -> id =", grid[row][col].id)
            else:
                print("Clique hors grille :", (mx,my), "->", (row,col))

    screen.fill((0,0,0))

    # draw all cells -Alex
    for row in grid:
        for cell in row:
            cell.draw(screen)

    #Draw arrow
    #Red arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3, end_row=7, end_col=7, color=RED, cell_size=CELL,
                    direction="down")
    #Green arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3, end_row=7, end_col=7, color=GREEN, cell_size=CELL,
                    direction="right")
    #Yellow arrow
    draw_wide_arrow(screen, start_row=8, start_col=6, base_width=3, end_row=7, end_col=7, color=YELLOW, cell_size=CELL,
                    direction="up")
    #Blue arrow
    draw_wide_arrow(screen, start_row=6, start_col=8, base_width=3, end_row=7, end_col=7, color=BLUE, cell_size=CELL,
                    direction="left")

    pygame.display.flip()
    pygame.display.update()

pygame.quit()