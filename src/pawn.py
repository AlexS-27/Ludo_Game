# src/pawn.py
class Pawn:
    def __init__(self, player, pawn_id):
        self.player = player
        self.pawn_id = pawn_id
        # position = None (en réserve), position = integer (sur plateau/safe path), is_finished = true (terminé)
        self.position = None
        self.is_finished = False

    def enter_board(self, board):
        # Cette fonction sera gérée par Game.try_to_release_pawn
        pass

    def can_move(self, steps, board):
        # Vérification complexe à implémenter, on le laisse dans Game pour l'instant
        return True

    def move(self, steps, board):
        # Mouvement géré par Game.try_to_move_pawn
        pass