from pawn import Pawn

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
            game_pawn = Pawn(self, i)
            self.pawns.append(game_pawn)

    def play_turn(self, dice_value, board):
        pass # to define later on

    def has_won(self):
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True