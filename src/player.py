"""
Ludo Game - Player Module
Description: Defines the Player class which manages pawn ownership,
             scoring, and victory conditions.
Authors: Alexandre Ramirez, Kilian Testard, Niels Delafontaine et Alex Kamano with help of IA

Date: 2025
"""

from src.pawn import Pawn

# Mapping of player indices to their respective board colors
PLAYER_COLORS = {
    1: "blue",
    2: "red",
    3: "green",
    4: "yellow"
}


class Player:
    """
    Represents a participant in the Ludo game.
    Manages the player's name, color, score, and set of four pawns.
    """

    def __init__(self, name, index):
        """
        Initializes a new player with a name and color based on their index.

        Args:
            name (str): The display name of the player.
            index (int): The player number (1-4) used to assign color.
        """
        self.name = name
        self.color = PLAYER_COLORS[index]
        self.score = 0
        self.pawns = []

        # Initialize 4 pawns for the player.
        # The pawn ID is crucial for positioning within the storage/home zones.
        for i in range(4):
            game_pawn = Pawn(self, i)
            self.pawns.append(game_pawn)

    # Note: The play_turn method was removed as the game is now UI-driven
    # (triggered by dice and pawn clicks). Movement logic has been moved
    # to Game.try_to_release_pawn and Game.try_to_move_pawn.

    def has_won(self):
        """
        Checks if the player has won the game.

        Returns:
            bool: True if all four pawns have reached the finish line, False otherwise.
        """
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True