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
            game_pawn = Pawn(self, i)
            self.pawns.append(game_pawn)

    def play_turn(self, dice_value, board):
        # define reserve/movable pawns
        reserve_pawns = []
        movable_pawns = []
        for p in self.pawns:
            if p.position is None and not p.is_finished:
                reserve_pawns.append(p)
        for p in self.pawns:
            if p.position is not None and not p.is_finished:
                movable_pawns.append(p)

    def has_won(self):
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True