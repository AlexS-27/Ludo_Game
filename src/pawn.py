class Pawn:
    def __init__(self, player, pawn_id):
        self.player = player
        self.pawn_id = pawn_id
        self.position = None # none == in reserve, integer == in play, is_finished = true == finished
        self.is_finished = False

    # function to place the pawn on its starting square
    def enter_board(self, board):
        # self.position = board.get_starting_position(self.player.color)
        self.position = 0 # temporary

    def can_move(self, steps, board):
        # check if the pawn can move, logic to be defined later on
        return True

    def move(self, steps, board):
        if self.can_move(steps, board):
            # movement logic to be defined later on
            pass