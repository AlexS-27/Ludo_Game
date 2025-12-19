# src/player.py
from src.pawn import Pawn

PLAYER_COLORS = {
    1: "blue",
    2: "red",
    3: "green",
    4: "yellow"
}

class Player:
    def __init__(self, name, index):
        self.name = name
        self.color = PLAYER_COLORS[index]
        self.pawns = []
        for i in range(4):
            # L'ID du pion est important pour le localiser dans la zone de stockage
            game_pawn = Pawn(self, i)
            self.pawns.append(game_pawn)

    # La méthode play_turn est retirée, car le jeu est maintenant piloté par l'UI (clic sur le dé, clic sur le pion).
    # La logique est déplacée dans Game.try_to_release_pawn et Game.try_to_move_pawn.

    def has_won(self):
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True