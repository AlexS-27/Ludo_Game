from pawn import Pawn

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pawns = []
        for i in range(4):
            game_pawn = Pawn(self, i)
            self.pawns.append(game_pawn)

    def play_turn(self, dice_value, board):
        pass # to define later on

    def has_won(self):
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True