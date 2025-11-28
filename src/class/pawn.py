class Pawn:
    def __init__(self, player, pawn_id):
        self.player = player
        self.pawn_id = pawn_id
        self.position = None
        self.is_finished = False

    def can_move(self, steps, board):
        # check if the pawn can move, logic to be defined later on
        return True

    def move(self, steps, board):
        if self.can_move(steps, board):
            # movement logic to be defined later on
            pass