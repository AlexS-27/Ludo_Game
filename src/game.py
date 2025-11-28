import random
from player import Player

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0
        self.board = None # to define more clearly after we finished working on the game board
        self.is_over = False

    def dice_roll(self):
        return random.randint(1,6)

    def next_player(self, last_roll):
        # roll a 6 = play another turn
        if last_roll == 6:
            return

        # use modulo to manage turn order (return to player[0] after player[3]'s turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)



    def start_game(self):
        while not self.is_over:
            player = self.players[self.current_player_index]
            dice = self.dice_roll()

            # pop-ups about whose turn it is and what number the dice rolled

            player.play_turn(dice, self.board)

            if player.has_won():
                self.is_over = True
            else:
                self.next_player()