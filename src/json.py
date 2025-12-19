# src/json.py
from src.Json_manager import *
from src.player import Player
from src.game import Game
from src.gamestate import GameState

def create_game(game_name, player_names):
    players = []
    players_data = []

    for idx, name in enumerate(player_names):
        player = Player(name, idx + 1)
        players.append(player)
        pawns_data = [{"pawn_id": p.pawn_id, "position": None, "is_finished": False}
                      for p in player.pawns]

        players_data.append({
            "name": player.name,
            "color": player.color,
            "pawns": pawns_data
        })

    game_state = GameState(
        players_data=players_data,
        current_player_index=0,
        board_data={},
        is_over=False
    )

    json_manager = JsonGameManager(game_name)
    json_manager.save(game_state)

    # On attache le nom à l'objet Game
    game = Game(players, grid=[], game_path_length=0)
    game.name = game_name
    return game

def save_game(game, game_name):
    """Sauvegarde le Game actuel via JsonManager"""
    json_manager = JsonGameManager(game_name)
    # On s'assure que l'objet game peut générer un snapshot
    json_manager.save(game.snapshot())

def load_game(game_name, grid=None, game_path_length=None):
    if grid is None: grid = []
    if game_path_length is None: game_path_length = 52

    json_manager = JsonGameManager(game_name)
    game_state = json_manager.load()

    if not game_state:
        return None

    players = []
    for idx, p_data in enumerate(game_state.players_data):
        player = Player(p_data["name"], idx + 1)
        for pawn, pawn_data in zip(player.pawns, p_data["pawns"]):
            pawn.position = pawn_data["position"]
            pawn.is_finished = pawn_data["is_finished"]
        players.append(player)

    game = Game(players, grid, game_path_length)
    game.current_player_index = game_state.current_player_index
    game.is_over = game_state.is_over
    game.name = game_name
    return game