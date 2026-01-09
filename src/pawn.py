"""
Ludo Game - Pawn Module
Description: Defines the Pawn class representing individual game pieces.
             Manages tracking of position, status, and ownership.
Authors: Alexandre Ramirez, Kilian Testard, Niels Delafontaine et Alex Kamano with help of IA
Date: 2025
"""


class Pawn:
    """
    Represents an individual game piece (pawn) on the Ludo board.
    """

    def __init__(self, player, pawn_id):
        """
        Initializes a pawn belonging to a specific player.

        Args:
            player (Player): The player object who owns this pawn.
            pawn_id (int): Unique identifier for the pawn (0-3).
        """
        self.player = player
        self.pawn_id = pawn_id

        # position = None: The pawn is currently in the storage/nest area.
        # position = int: The pawn is on the common path or player-specific safe path.
        self.position = None

        # is_finished = True: The pawn has successfully reached the home goal.
        self.is_finished = False