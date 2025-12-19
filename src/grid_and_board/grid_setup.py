# src/grid_and_board/grid_setup.py
from src.grid_and_board.cell import *

# Ajout pour la logique de jeu (ID du chemin de départ, basé sur setup_game_path)
PLAYER_START_POSITIONS = {
    "blue": 1,  # Case (0, 7)
    "yellow": 15,  # Case (7, 14)
    "green": 29,  # Case (14, 7)
    "red": 43,  # Case (7, 0)
}

# (Ajout pour référence dans game.py, pas utilisé dans la V1)
PLAYER_ENTRY_CELLS = {
    "blue": (1, 8),
    "yellow": (13, 8),
    "green": (8, 1),
    "red": (6, 1)
}


def create_grid(rows, cols, cell_width, cell_height):
    grid = [[Cell(r, c, cell_width, cell_height) for c in range(cols)] for r in range(rows)]
    return grid


def setup_home_and_storage(grid, colors):
    # ... (le reste de la fonction est inchangé) ...
    # Zones home_area
    home_areas = {
        "RED": (0, 0),
        "BLUE": (0, 9),
        "YELLOW": (9, 9),
        "GREEN": (9, 0)
    }

    # Map pour localiser les pions en réserve (couleur, pawn_id) -> (row, col)
    storage_cells = {}

    for color_name, (base_r, base_c) in home_areas.items():
        # ... (le reste du code pour HOME_AREA) ...
        for r in range(base_r, base_r + 6):
            for c in range(base_c, base_c + 6):
                grid[r][c].cell_type = HOME_AREA
                grid[r][c].color = colors[color_name]

    # Cases de stockage dans home_area (4 par zone)
    storage_offsets = [(1, 1), (1, 4), (4, 1), (4, 4)]
    storage_id_counter = 100
    pawn_id_counter = 0  # Le pawn_id va de 0 à 3

    for color_name, (base_r, base_c) in home_areas.items():
        pawn_id_counter = 0  # Réinitialiser pour chaque couleur
        for dr, dc in storage_offsets:
            r = base_r + dr
            c = base_c + dc
            grid[r][c].cell_type = STORAGE
            grid[r][c].id = storage_id_counter
            grid[r][c].color = WHITE

            # Stocker l'information de la case de stockage pour le dessin/clic des pions
            storage_cells[(color_name.lower(), pawn_id_counter)] = {'row': r, 'col': c, 'id': storage_id_counter}

            storage_id_counter += 1
            pawn_id_counter += 1

    return storage_cells  # Retourner la carte des positions de stockage


def setup_game_path(grid):
    # Chemin jouable (indexation 1 → 56)
    # ... (le reste de la fonction est inchangé, assurez-vous que le compteur final est 56) ...
    # Le reste du code de cette fonction est inchangé, il retourne game_id_counter qui est 57 si 56 cases sont créées (la dernière étant 56)
    game_id_counter = 1

    # ... (toute la logique de création des chemins) ...

    # Chemin horizontal en haut
    for c in range(6, 9):
        grid[0][c].cell_type = NORMAL_HORIZONTAL
        grid[0][c].id = game_id_counter
        game_id_counter += 1
    # ... (le reste du chemin principal) ...

    # Chemin horizontal rouge (la dernière du chemin principal est 56)
    for c in range(1, 6):
        grid[6][c].cell_type = NORMAL_HORIZONTAL
        grid[6][c].id = game_id_counter
        game_id_counter += 1

    # Chemin vertical rouge (la dernière est 56)
    for r in range(5, 0, -1):
        grid[r][6].cell_type = NORMAL_VERTICAL
        grid[r][6].id = game_id_counter
        game_id_counter += 1

    # Le compteur doit être 57 après 56 cases jouables.

    # Safe paths (chemins finaux vers le centre) - identifiants 200,300,400,500
    # ... (reste inchangé) ...

    return game_id_counter - 1  # Retourne la longueur du chemin (56)