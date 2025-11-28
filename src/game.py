import random
from player import Player
from gamestate import GameState

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


    def snapshot(self):
        players_data = []

        for player in self.players:
            pawns_data = []
            for p in player.pawns:
                pawns_data.append({
                    "pawn_id": p.pawn_id,
                    "position": p.position,
                    "is_finished": p.is_finished,
                })
            players_data.append({
                "name": player.name,
                "color": player.color,
                "pawns": pawns_data,
            })

        board_data = {
            # to be added later
        }

        return GameState(
            players_data=players_data,
            current_player_index=self.current_player_index,
            board_data=board_data,
            is_over=self.is_over,
        )


    # next needed methods:
    # save the snapshot in JSON,
    # load the snapshot from JSON,
    # rebuilding of the game from the snapshot's info