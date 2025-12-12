class GameState:
    def __init__(self, players_data, current_player_index, board_data, is_over):
        self.players_data = players_data
        self.current_player_index = current_player_index
        self.board_data = board_data
        self.is_over = is_over