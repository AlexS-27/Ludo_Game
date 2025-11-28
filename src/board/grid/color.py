from settings import RED, GREEN, BLUE, YELLOW

def color_ludo(grid):
    """Applique les couleurs à la grille (zones, safe paths, entrées)."""
    # Red zone
    for r in range(0,6):
        for c in range(0,6):
            grid[r][c].color = RED
            grid[r][c].border_width = 0
    # Blue zone
    for r in range(0,6):
        for c in range(9,15):
            grid[r][c].color = BLUE
            grid[r][c].border_width = 0
    # Yellow zone
    for r in range(9,15):
        for c in range(9,15):
            grid[r][c].color = YELLOW
            grid[r][c].border_width = 0
    # Green zone
    for r in range(9,15):
        for c in range(0,6):
            grid[r][c].color = GREEN
            grid[r][c].border_width = 0
