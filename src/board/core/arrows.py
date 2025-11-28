import pygame
from settings import RED

def draw_wide_arrow(surface, start_row, start_col, base_width=3, end_row=None, end_col=None, color=RED,
                    cell_width=50, cell_height=50, direction="down"):
    """
    Dessine une flèche large :
    - base_width : nombre de cases pour la base
    - start_row, start_col : case de départ
    - end_row, end_col : case d'arrivée (pointe)
    """
    if end_row is None:
        end_row = start_row + 1
    if end_col is None:
        end_col = start_col

    x_start = start_col * cell_width
    y_start = start_row * cell_height
    x_end = end_col * cell_width + cell_width // 2
    y_end = end_row * cell_height + cell_height // 2

    if direction == "down":
        x1, y1 = x_start, y_start
        x2, y2 = x_start + base_width * cell_width, y_start
    elif direction == "up":
        x1, y1 = x_start, y_start + cell_height
        x2, y2 = x_start + base_width * cell_width, y_start + cell_height
    elif direction == "right":
        x1, y1 = x_start, y_start
        x2, y2 = x_start, y_start + base_width * cell_height
    elif direction == "left":
        x1, y1 = x_start + cell_width, y_start
        x2, y2 = x_start + cell_width, y_start + base_width * cell_height

    points = [(x1, y1), (x2, y2), (x_end, y_end)]
    pygame.draw.polygon(surface, color, points)
