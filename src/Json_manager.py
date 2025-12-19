# src/json_manager.py
import json
import os
from src.gamestate import GameState
from pathlib import Path
def _default_json_path():
    src_dir = Path(__file__).resolve().parent   # .../project/src
    project_root = src_dir.parent                # .../project
    json_dir = project_root / "docs" / "json"
    # create folder if missing
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir
    return json_path
SAVE_DIR = "../docs/json/"
os.makedirs(SAVE_DIR, exist_ok=True)

class JsonGameManager:
    def __init__(self, game_name: str):
        self.game_name = game_name
        self.path = self._get_path()

    def _get_path(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
        return os.path.join(SAVE_DIR, f"{self.game_name}.json")

    # ==========================
    # SAUVEGARDE
    # ==========================
    def save(self, game_state: GameState):
        """
        Sauvegarde un GameState (ou Game via snapshot)
        """
        # Si c'est un Game, prends snapshot
        if hasattr(game_state, "snapshot"):
            game_state = game_state.snapshot()

        data = {
            "players": game_state.players_data,
            "current_player_index": game_state.current_player_index,
            "grid": self.serialize_grid(game_state.board_data),
            "game_path_length": 52,
            "is_over": game_state.is_over,
        }

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _serialize_player(self, player):
        return {
            "name": player.name,
            "color": player.color,
            "pawns": [{"pawn_id": p.pawn_id, "position": p.position, "is_finished": p.is_finished} for p in player.pawns]
        }

    @staticmethod
    def serialize_grid(grid):
        """Convertir la grille en format JSON sérialisable"""
        if not grid:  # Si la grille est vide ({}) ou None
            return []

        # Si grid est une liste de listes (votre structure habituelle)
        try:
            rows = len(grid)
            cols = len(grid[0])
            data = []
            for r in range(rows):
                row_data = []
                for c in range(cols):
                    cell = grid[r][c]
                    row_data.append({
                        "id": cell.id,
                        "cell_type": cell.cell_type
                    })
                data.append(row_data)
            return data
        except (TypeError, IndexError):
            return []

    @staticmethod
    def deserialize_grid(data):
        """Reconstruire la grille depuis le JSON"""
        from src.grid_and_board.cell import Cell
        grid = []
        for r, row_data in enumerate(data):
            row = []
            for c, cell_data in enumerate(row_data):
                cell = Cell(row=r, col=c, cell_type=cell_data["cell_type"], id=cell_data["id"])
                row.append(cell)
            grid.append(row)
        return grid

    # ==========================
    # CHARGEMENT
    # ==========================
    def load(self):
        if not os.path.exists(self.path):
            return None

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # On extrait les données brutes pour que json.py puisse les utiliser
        # OU on retourne un objet GameState.
        # Pour coller à votre code actuel dans json.py, modifions load() ainsi :

        from src.gamestate import GameState

        return GameState(
            players_data=data["players"],
            current_player_index=data["current_player_index"],
            board_data=data.get("grid", []),  # On récupère grid ici
            is_over=data["is_over"]
        )
