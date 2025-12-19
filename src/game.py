# src/game.py
import random
from src.gamestate import GameState
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH, STORAGE

# Ces positions correspondent aux IDs générés dans grid_setup.py
PLAYER_START_POSITIONS = {
    "blue": 1,  # Départ Bleu
    "red": 43,  # Départ Rouge (selon setup_game_path)
    "green": 29,  # Départ Vert
    "yellow": 15  # Départ Jaune
}

ROLL_TO_RELEASE = 5
MAX_COMMON_PATH = 52  # Le nombre total de cases sur l'anneau extérieur


class Game:
    def __init__(self, players, grid, game_path_length):
        self.players = players
        self.current_player_index = 0
        self.grid = grid
        self.is_over = False
        self.rolled_dice = None
        self.game_path_length = game_path_length
        self.message = "It is Player 1 (blue)'s turn to roll the dice."

        # Mapping pour trouver rapidement les cellules par ID
        self.game_cells = self._create_game_cells_map()

    def set_message(self, msg):
        self.message = msg

    def _create_game_cells_map(self):
        """ Crée un dictionnaire ID -> {cell, row, col} pour un accès instantané """
        game_cells = {}
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                cell = self.grid[r][c]
                if cell.id is not None:
                    game_cells[cell.id] = {'cell': cell, 'row': r, 'col': c}
        return game_cells

    def get_cell_by_position(self, position_id):
        return self.game_cells.get(position_id)

    def get_pawns_on_cell(self, row, col):
        """ Trouve tous les pions présents sur une coordonnée précise """
        pawns_on_cell = []
        for player in self.players:
            for pawn in player.pawns:
                if pawn.position is not None:
                    cell_info = self.get_cell_by_position(pawn.position)
                    if cell_info and cell_info['row'] == row and cell_info['col'] == col:
                        pawns_on_cell.append(pawn)
        return pawns_on_cell

    # Dans src/game.py

    def can_player_move(self, dice_value):
        player = self.players[self.current_player_index]

        for pawn in player.pawns:
            if pawn.is_finished:
                continue

            # Cas 1 : Le pion est dans le storage
            if pawn.position is None:
                if dice_value == ROLL_TO_RELEASE:
                    # Peut sortir si la case de départ n'est pas occupée par lui-même
                    start_pos_id = PLAYER_START_POSITIONS[player.color]
                    if not any(p.position == start_pos_id for p in player.pawns):
                        return True

            # Cas 2 : Le pion est déjà sur le plateau
            else:
                # Pour l'instant on retourne True, mais idéalement il faudrait vérifier
                # si le mouvement ne dépasse pas la zone de victoire (Safe Path)
                return True

        return False

    def next_player(self):
        """ Passe au joueur suivant, sauf si un 6 est tiré """
        if self.rolled_dice == 6:
            self.set_message(f"{self.players[self.current_player_index].name} rolled a 6! Play again.")
        else:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            curr = self.players[self.current_player_index]
            self.set_message(f"It's {curr.name} ({curr.color})'s turn.")

        self.rolled_dice = None

    def try_to_release_pawn(self, pawn, dice_value):
        """ Tente de sortir un pion du storage vers la case de départ """
        if dice_value != ROLL_TO_RELEASE:
            self.set_message(f"Need a {ROLL_TO_RELEASE} to release, not {dice_value}.")
            return False

        start_pos_id = PLAYER_START_POSITIONS[pawn.player.color]

        # Vérifier si la case de départ est déjà occupée par un de ses propres pions
        my_pawns_at_start = [p for p in pawn.player.pawns if p.position == start_pos_id]
        if my_pawns_at_start:
            self.set_message("Starting cell is blocked by your own pawn.")
            return False

        # Gérer la capture si un ennemi est sur la case
        self.check_collision(start_pos_id)

        pawn.position = start_pos_id
        self.set_message(f"Pawn released to position {start_pos_id}!")
        return True

    def try_to_move_pawn(self, pawn, dice_value):
        """ Calcule et applique le mouvement d'un pion sur l'anneau """
        if pawn.player != self.players[self.current_player_index]:
            self.set_message("Not your turn / Not your pawn.")
            return False

        if pawn.position is None:
            return False

        # Logique de boucle sur l'anneau (1 à 56)
        new_pos_id = pawn.position + dice_value
        if new_pos_id > MAX_COMMON_PATH:
            new_pos_id -= MAX_COMMON_PATH

        # Vérifier si la case d'arrivée est occupée par soi-même
        my_pawns_at_dest = [p for p in pawn.player.pawns if p.position == new_pos_id]
        if my_pawns_at_dest:
            self.set_message("Target cell is occupied by your own pawn.")
            return False

        # Gérer la capture d'un pion adverse
        self.check_collision(new_pos_id)

        pawn.position = new_pos_id
        self.set_message(f"Pawn moved to {new_pos_id}.")
        return True

    def check_collision(self, position_id):
        """ Renvoie les pions adverses en storage s'ils sont sur la case d'arrivée """
        current_player = self.players[self.current_player_index]
        for player in self.players:
            if player == current_player:
                continue

            for pawn in player.pawns:
                if pawn.position == position_id:
                    pawn.position = None  # Retour en storage
                    self.set_message(f"Captured {player.color}'s pawn!")

    def post_move_cleanup(self):
        """ Vérifie la victoire et passe au tour suivant """
        player = self.players[self.current_player_index]
        if player.has_won():
            self.is_over = True
            self.set_message(f"GAME OVER - {player.name} WON!")
        else:
            self.next_player()

    def snapshot(self):
        players_data = []
        for player in self.players:
            pawns_data = [{"pawn_id": p.pawn_id, "position": p.position, "is_finished": p.is_finished} for p in
                          player.pawns]
            players_data.append({"name": player.name, "color": player.color, "pawns": pawns_data})

        return GameState(players_data, self.current_player_index, {}, self.is_over)