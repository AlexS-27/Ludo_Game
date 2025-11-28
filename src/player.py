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

        # for now, a 5 roll automatically releases a pawn from reserve
        if dice_value == 5 and reserve_pawns:
            released_pawn = reserve_pawns[0]
            released_pawn.enter_board(board)
            return

        # for now, players automatically move their first movable pawn on their turn
        if movable_pawns:
            moving_pawn = movable_pawns[0]
            moving_pawn.move(dice_value, board)
            return

    def has_won(self):
        for p in self.pawns:
            if not p.is_finished:
                return False
        return True