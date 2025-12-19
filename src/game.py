# src/game.py
import random
from src.gamestate import GameState
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH, STORAGE

# Ces positions correspondent aux IDs générés dans grid_setup.py
PLAYER_START_POSITIONS = {
    "blue": 13,  # Départ Bleu
    "red": 52,  # Départ Rouge (selon setup_game_path)
    "green": 39,  # Départ Vert
    "yellow": 26  # Départ Jaune
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

    def can_player_move(self, dice_value):
        player = self.players[self.current_player_index]

        for pawn in player.pawns:
            if pawn.position is None:
                if dice_value == ROLL_TO_RELEASE:
                    start_pos_id = PLAYER_START_POSITIONS[player.color]
                    for p in player.pawns:
                        if not any(p.position == start_pos_id for p in player.pawns):
                            return True
            elif not pawn.is_finished:
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
        if pawn.player != self.players[self.current_player_index] or pawn.position is None:
            return False

        current_pos = pawn.position
        BIFURCATION_LOGIC = {
            "red": {"exit_node": 51, "safe_start": 200},
            "yellow": {"exit_node": 25, "safe_start": 300},
            "green": {"exit_node": 38, "safe_start": 400},
            "blue": {"exit_node": 12, "safe_start": 500}
        }

        logic = BIFURCATION_LOGIC[pawn.player.color]
        last_cell_id = logic["safe_start"] + 4

        # --- LOGIQUE DE VICTOIRE IMMÉDIATE ---

        # 1. Si le pion est déjà dans le safe path
        if current_pos >= 200:
            distance_to_finish = last_cell_id - current_pos
            if dice_value >= distance_to_finish:
                self._validate_pawn_finish(pawn)
                return True
            new_pos_id = current_pos + dice_value

        # 2. Si le pion est sur l'anneau et s'approche de sa sortie
        else:
            # On calcule la position théorique
            new_pos_id = current_pos + dice_value

            # S'il dépasse son point de bifurcation
            if current_pos <= logic["exit_node"] and new_pos_id > logic["exit_node"]:
                steps_after_exit = new_pos_id - logic["exit_node"]
                # Si le nombre de pas après la sortie atteint ou dépasse la fin du safe path (5 cases)
                if steps_after_exit >= 5:
                    self._validate_pawn_finish(pawn)
                    return True
                else:
                    new_pos_id = logic["safe_start"] + (steps_after_exit - 1)

            # Boucle normale sur l'anneau extérieur
            elif new_pos_id > MAX_COMMON_PATH:
                new_pos_id -= MAX_COMMON_PATH

        # --- VÉRIFICATIONS STANDARDS ---
        my_pawns_at_dest = [p for p in pawn.player.pawns if p.position == new_pos_id and p != pawn]
        if my_pawns_at_dest:
            self.set_message("Target cell is occupied by your own pawn.")
            return False

        self.check_collision(new_pos_id)
        pawn.position = new_pos_id

        # Cas où il tombe pile sur la dernière case via le mouvement normal
        if pawn.position == last_cell_id:
            self._validate_pawn_finish(pawn)

        return True

    def _validate_pawn_finish(self, pawn):
        """ Utilitaire pour sortir le pion et marquer le point """
        pawn.is_finished = True
        pawn.position = None  # Le pion n'est plus sur le plateau
        self.set_message(f"Great! A {pawn.player.color} pawn has finished its journey!")

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