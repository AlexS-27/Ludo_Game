from src.board.grid.cell import Cell
from settings import WHITE

def create_grid(rows, cols, cell_width, cell_height):
    return [[Cell(r, c, cell_width, cell_height) for c in range(cols)] for r in range(rows)]

def setup_home_and_storage(grid, colors):
    home_areas = {
        "RED": (0, 0),
        "BLUE": (0, 9),
        "YELLOW": (9, 9),
        "GREEN": (9, 0)
    }
    storage_offsets = [(1,1), (1,4), (4,1), (4,4)]
    storage_id_counter = 100

    for color_name, (base_r, base_c) in home_areas.items():
        for r in range(base_r, base_r + 6):
            for c in range(base_c, base_c + 6):
                grid[r][c].cell_type = "home_area"
                grid[r][c].color = colors[color_name]
        for dr, dc in storage_offsets:
            r = base_r + dr
            c = base_c + dc
            grid[r][c].cell_type = "storage"
            grid[r][c].id = storage_id_counter
            grid[r][c].color = WHITE
            storage_id_counter += 1

def setup_game_path(grid):
    """Ajoute les IDs aux chemins et safe paths (à compléter)."""
    pass
