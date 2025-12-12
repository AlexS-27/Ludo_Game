# main.py
import pygame
from src.grid_and_board.cell import Cell, RED, GREEN, BLUE, YELLOW, WHITE
from src.grid_and_board.board import color_ludo
from src.grid_and_board.grid_setup import create_grid, setup_home_and_storage, setup_game_path
from src.grid_and_board.arrows import draw_entry_arrows

pygame.init()

# Window
screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
pygame.display.set_caption("Ludo Game")

# Grid configuration
ROWS, COLS = 15, 15
CELL_WIDTH = 50
CELL_HEIGHT = 50

# Colors mapping (used by setup_home_and_storage)
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}

# Initialize grid
grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)

# Apply coloring (board.py)
color_ludo(grid)

# Setup home areas and storage cells
setup_home_and_storage(grid, colors)

# Setup paths
setup_game_path(grid)

# Main loop
run = True
clock = pygame.time.Clock()

while run:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // CELL_WIDTH
            row = my // CELL_HEIGHT
            if 0 <= row < ROWS and 0 <= col < COLS:
                clicked_cell = grid[row][col]
                print(f"Case cliquée: ID={clicked_cell.id}, Type={clicked_cell.cell_type}")

    screen.fill((0, 0, 0))

    # Draw grid
    for row in grid:
        for cell in row:
            cell.draw(screen)

    # Draw arrival arrows
    draw_entry_arrows(screen, CELL_WIDTH, CELL_HEIGHT)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
