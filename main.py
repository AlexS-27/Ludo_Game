# main.py
import pygame
from settings import ROWS, COLS, CELL_WIDTH, CELL_HEIGHT, RED, GREEN, BLUE, YELLOW, WHITE
from src.board.grid.grid_setup import create_grid, setup_home_and_storage
from src.board.grid.color import color_ludo
from src.graphics.draw import draw_grid


def main():
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_WIDTH, ROWS * CELL_HEIGHT))
    pygame.display.set_caption("Ludo Grid Test")
    clock = pygame.time.Clock()

    # Crée la grille
    grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)

    # Applique les couleurs Ludo
    colors = {"RED": RED, "GREEN": GREEN, "BLUE": BLUE, "YELLOW": YELLOW}
    setup_home_and_storage(grid, colors)
    color_ludo(grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
