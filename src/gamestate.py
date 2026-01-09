"""
Ludo Game - Core Game Logic & State Management
Description: Controls the flow of the game, including turn transitions, 
             pawn movement validation, and win condition checking.
Authors: Alexandre Ramirez, Kilian Testard, Niels Delafontaine et Alex Kamano with help of IA
Date: 2025
"""

import pygame
from src.grid_and_board.cell import STORAGE


class GameState:
    """
    Manages the overall game state, player turns, and interaction 
    between the board grid and the pawns.
    """

    def __init__(self, players_data, current_player_index, board_data, is_over):
        self.players_data = players_data
        self.current_player_index = current_player_index
        self.board_data = board_data
        self.is_over = is_over

    def set_message(self, text):
        """Updates the status message displayed in the UI."""
        self.message = text

    def next_turn(self):
        """Transitions the game to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.rolled_dice = None
        self.set_message(f"It is {self.players[self.current_player_index].name}'s turn.")

    def get_cell_by_position(self, pos_id):
        """
        Locates a cell in the grid based on its unique position ID.

        Args:
            pos_id (int): The ID of the cell to find.
        Returns:
            dict: Dictionary containing 'row' and 'col' if found, None otherwise.
        """
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c].id == pos_id:
                    return {'row': r, 'col': c}
        return None

    def get_pawns_on_cell(self, row, col):
        """
        Retrieves all pawns currently occupying a specific grid coordinate.
        """
        pawns_found = []
        cell_id = self.grid[row][col].id

        for player in self.players:
            for pawn in player.pawns:
                # Check both path position and storage location
                if pawn.position == cell_id and cell_id is not None:
                    pawns_found.append(pawn)
                # Check storage specifically if position is None
                elif pawn.position is None and self.grid[row][col].cell_type == STORAGE:
                    # Logic here depends on your setup_home_and_storage mapping
                    pass
        return pawns_found

    def can_player_move(self, roll):
        """
        Determines if the current player has any valid moves with the rolled value.
        """
        player = self.players[self.current_player_index]
        for pawn in player.pawns:
            if pawn.is_finished:
                continue
            # A 6 (or 5 depending on your rules) allows exiting storage
            if pawn.position is None and roll == 5:
                return True
            # Any pawn on the board can potentially move
            if pawn.position is not None:
                return True
        return False

    def try_to_release_pawn(self, pawn, roll):
        """
        Attempts to move a pawn from the storage area to the starting cell.
        """
        if roll == 5:
            # Logic to set pawn.position to the player's start ID
            pawn.position = 0  # Example start position
            self.players[self.current_player_index].score += 10
            return True
        return False

    def try_to_move_pawn(self, pawn, roll):
        """
        Updates pawn position based on dice roll and validates movement.
        """
        # Example logic for moving along the path
        pawn.position += roll
        self.players[self.current_player_index].score += roll

        # Check if pawn reached the end
        if pawn.position >= self.path_length:
            pawn.is_finished = True
            self.players[self.current_player_index].score += 100

        return True

    def post_move_cleanup(self):
        """
        Handles turn conclusion logic, such as checking for a winner 
        or switching to the next player.
        """
        if self.players[self.current_player_index].has_won():
            self.set_message(f"GAME OVER! {self.players[self.current_player_index].name} WINS!")
            self.game_over = True
        else:
            self.next_turn()
"""
    def __init__(self, players, grid, path_length):
        
        Initializes the game engine.

        Args:
            players (list): List of Player objects.
            grid (list): 2D list representing the board cells.
            path_length (int): Total number of cells in the main game path.
        
        self.players = players
        self.grid = grid
        self.path_length = path_length
        self.current_player_index = 0
        self.rolled_dice = None
        self.message = f"Welcome! {self.players[0].name}'s turn."
        self.game_over = False
"""