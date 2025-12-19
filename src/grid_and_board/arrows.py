import pygame

# Créer avec l'aide de chatGPT -Alex
def draw_wide_arrow(surface, start_row, start_col, base_width=3, end_row=None, end_col=None,
                    color=(255,0,0), cell_width=40, cell_height=40, direction="down",
                    offset_x=0, offset_y=0):
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

    # Coordinates of the base origin (top-left of starting cell)
    x_start = offset_x + start_col * cell_width
    y_start = offset_y + start_row * cell_height

    # Coordinates of the arrow tip (center of target cell)
    x_end = offset_x + end_col * cell_width + cell_width // 2
    y_end = offset_y + end_row * cell_height + cell_height // 2

    if direction == "down":
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
    else:
        return  # Unsupported direction

    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x_end, y_end)])


def draw_entry_arrows(surface, start_row, start_col, base_width,
                      end_row, end_col, color,
                      cell_width, cell_height,
                      direction,
                      offset_x, offset_y):
    from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW

    # Rouge (Haut vers Centre)
    draw_wide_arrow(surface, 6, 6, 3, 7, 7, RED, cell_width, cell_height, "right", offset_x, offset_y)
    # Vert (Bas vers Centre)
    draw_wide_arrow(surface, 6, 6, 3, 7, 7, GREEN, cell_width, cell_height, "down", offset_x, offset_y)
    # Jaune (Droite vers Centre)
    draw_wide_arrow(surface, 6, 8, 3, 7, 7, YELLOW, cell_width, cell_height, "left", offset_x, offset_y)
    # Bleu (Gauche vers Centre)
    draw_wide_arrow(surface, 8, 6, 3, 7, 7, BLUE, cell_width, cell_height, "up", offset_x, offset_y)