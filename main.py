import pygame

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()

#setup window's title
pygame.display.set_caption("Ludo Game")

# define game variable
ROWS, COLS = 15, 15
CELL = 40

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Cell:
    def __init__(self, row, col, size, id):
        self.row = row
        self.col = col
        self.size = size
        self.id = id
        self.color = WHITE

    def draw(self, surface):
        x = self.col * self.size
        y = self.row * self.size
        pygame.draw.rect(surface, self.color, (x, y, self.size, self.size))
        pygame.draw.rect(surface, BLACK, (x , y, self.size, self.size), 1)

#create the grill + id
grid = []
id_counter = 0

for row in range(ROWS):
    grid.append([])
    for col in range(COLS):
        grid[row].append(Cell(row, col, CELL, id_counter))
        id_counter += 1


def color_ludo():
    #zone rouge
    for r in range(0,6):
        for c in range(0,6):
            grid[r][c].color = RED

    for r in range(0,6):
        for c in range(9,15):
            grid[r][c].color = BLUE

    for r in range(9,15):
        for c in range(9,15):
            grid[r][c].color = YELLOW

    for r in range(9,15):
        for c in range(0,6):
            grid[r][c].color = GREEN

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

        #Cliquer : Montre l'id de la case
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = my // CELL
            row = mx // ROWS
            print("Case cliqué -> id =", grid[row][col].id)

    screen.fill((0,0,0))

    #dessiner toutes les cases
    for row in grid:
        for cell in row:
            cell.draw(screen)

    pygame.display.flip()

pygame.quit()