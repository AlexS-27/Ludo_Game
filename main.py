import pygame
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW
from src.grid_and_board.board import color_ludo
from src.grid_and_board.arrows import draw_wide_arrow
from src.grid_and_board.grid_setup import create_grid, setup_home_and_storage, setup_game_path

pygame.init()
#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()
#setup window's title
pygame.display.set_caption("Ludo Game")

# Grid
ROWS, COLS = 15, 15
CELL_WIDTH, CELL_HEIGHT = 50, 50
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}

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


grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)
color_ludo(grid)
setup_home_and_storage(grid, colors)
setup_game_path(grid)

#laod image

#main loop
run = True
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
