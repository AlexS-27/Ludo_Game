import random
from src.player import Player
from src.gamestate import GameState
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH, STORAGE
#from src.grid_and_board.grid_setup import PLAYER_START_POSITIONS, PLAYER_ENTRY_CELLS # Nécessite une MàJ de grid_setup

ROLL_TO_RELEASE = 5
START_POSITION_ID = 1

class Game:
    def __init__(self, players, grid, game_path_length):
        self.players = players
        self.current_player_index = 0
        self.grid = grid
        self.is_over = False
        self.rolled_dice = None # dice roll for current turn
        self.game_path_length = game_path_length # max lenght of game track (56)
        self.message = "It is Player 1 (blue)'s turn to roll the dice.."

        # precalculate grid info (from AI)
        self.game_cells = self._create_game_cells_map()
        self.storage_cells_map = self._create_storage_cells_map()

    def set_message(self, msg):
        self.message = msg

    # from AI
    def _create_game_cells_map(self):
        game_cells = {}
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                cell = self.grid[r][c]
                if cell.id is not None and cell.cell_type in [NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH, STORAGE]:
                    game_cells[cell.id] = {'cell': cell, 'row': r, 'col': c}
        return game_cells

    # from AI
    def _create_storage_cells_map(self):
        storage_map = {}
        for player in self.players:
            for pawn in player.pawns:
                pass

    def get_cell_by_position(self, position_id):
        # return the cell object and its coordinates from its position_id
        return self.game_cells.get(position_id)

    def get_pawns_on_cell(self, row, col):
        # return the list of pawns on the cell
        pawns_on_cell = []
        target_cell = self.grid[row][col]
        for player in self.players:
            for pawn in player.pawns:
                cell_info = self.get_cell_by_position(pawn.position)
                if cell_info and cell_info['row'] == row and cell_info['col'] == col:
                    pawns_on_cell.append(pawn)
                elif pawn.position is None and target_cell.cell_type == STORAGE:
                    pass

        return pawns_on_cell

    def next_player(self):
        # roll a 6 = play another turn
        if self.rolled_dice == 6:
            self.set_message("You rolled a 6, play again !")
        else:
            # use modulo to manage turn order (return to player[0] after player[3]'s turn
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            new_player_name = self.players[self.current_player_index].name
            new_player_color = self.players[self.current_player_index].color
            self.set_message(f"It's {new_player_name} ({new_player_color})'s turn to play.")

        # Reset the dice for next turn
        self.rolled_dice = None

    # with AI
    def try_to_release_pawn(self, pawn, dice_value):
        player_color = pawn.player.color
        if dice_value == ROLL_TO_RELEASE:
            start_pos_id = PLAYER_START_POSITIONS[player_color]

            # Check if starting cell is occupied by another pawn
            pawns_at_start = [p for p in self.players[self.current_player_index].pawns if p.position == start_pos_id]

            # If the starting cell is occupied by a pawn of the same player, entering the board is impossible
            if pawns_at_start:
                self.set_message("One of your pawns already occupies you starting cell.")
                return False

            # Successfully entering the board
            pawn.position = start_pos_id
            self.set_message(f"Your pawn entered the board ! (ID: {start_pos_id})")
            return True
        else:
            return False

    def try_to_move_pawn(self, pawn, dice_value):
        if pawn.player != self.players[self.current_player_index]:
            self.set_message("This is not your pawn.")
            return False

        current_pos = pawn.position


        if current_pos is not None:
            # New position on the board (jusqu'à 56)
            new_pos_id = current_pos + dice_value

            # TODO: Implémenter la logique d'entrée dans le safe path
            # For now, we loop on the board
            if new_pos_id > self.game_path_length:
                # Ignore the move if it goes beyond the end of the track (for now)
                self.set_message("Move goes too far ! (end of track is not managed yet).")
                return False

            # Successful move
            pawn.position = new_pos_id
            self.set_message(f"Pawn moved to position: {new_pos_id}.")
            return True

        return False

    def post_move_cleanup(self):
        # cleanup after successful move
        # TODO: Implement collision and pawn capture

        # win check
        player = self.players[self.current_player_index]
        if player.has_won():
            self.is_over = True
            self.set_message(f"Congrats, {player.name} won the game !")

        # Switch to the next player
        self.next_player()

    def snapshot(self):
        players_data = []

        for player in self.players:
            pawns_data = []
            for p in player.pawns:
                pawns_data.append({
                    "pawn_id": p.pawn_id,
                    "position": p.position,
                    "is_finished": p.is_finished,
                })
            players_data.append({
                "name": player.name,
                "color": player.color,
                "pawns": pawns_data,
            })

        board_data = {
            # to be added later
        }

        return GameState(
            players_data=players_data,
            current_player_index=self.current_player_index,
            board_data=board_data,
            is_over=self.is_over,
        )


    # next needed methods:
    # save the snapshot in JSON,
    # load the snapshot from JSON,
    # rebuilding of the game from the snapshot's info