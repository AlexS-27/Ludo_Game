import pygame

# Créer la
# Avec l'aide de chatGPT -Alex
def draw_wide_arrow(surface, start_row, start_col, base_width=3, end_row=None, end_col=None, color=(255,0,0), cell_width=40, cell_height = 40,  direction="down"):
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
