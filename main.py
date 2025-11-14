import pygame

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()

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

class Cell:
    def __init__(self, row, col, width, height, id):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.id = id
        self.color = WHITE

    def draw(self, surface):
        x = self.col * self.width
        y = self.row * self.height
        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (x, y, self.width, self.height), 1)

# create the grid + id
grid = []
id_counter = 0

for row in range(ROWS):
    grid.append([])
    for col in range(COLS):
        grid[row].append(Cell(row, col, CELL_WIDTH, CELL_HEIGHT, id_counter))
        id_counter += 1

def color_ludo():
    # zone rouge
    for r in range(0, 6):
        for c in range(0, 6):
            grid[r][c].color = RED

    # zone bleue
    for r in range(0, 6):
        for c in range(9, 15):
            grid[r][c].color = BLUE

    # zone jaune
    for r in range(9, 15):
        for c in range(9, 15):
            grid[r][c].color = YELLOW

    # zone verte
    for r in range(9, 15):
        for c in range(0, 6):
            grid[r][c].color = GREEN

color_ludo()

run = True

while run:

    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            run = False

        # click detection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // CELL_WIDTH
            row = my // CELL_HEIGHT
            print("Case cliquée -> id =", grid[row][col].id)

    screen.fill((0, 0, 0))

    # draw all cells
    for row in grid:
        for cell in row:
            cell.draw(screen)

    pygame.display.flip()

pygame.quit()
