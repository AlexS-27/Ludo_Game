import pygame
import sys
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, WHITE, BLACK, Cell, BORDER, STORAGE, HOME_AREA, \
    NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH
from src.grid_and_board.board import color_ludo
from src.grid_and_board.arrows import draw_entry_arrows
from src.grid_and_board.grid_setup import create_grid, setup_home_and_storage, setup_game_path
from src.dice_roll import Dice
from src.linkwithdatabase import get_connection
from src.login import run_launcher
from src.game import Game
from src.player import Player

# --- Setup DB ---
custom_path = "./docs/Database/ludo.db"
conn = get_connection(custom_path)
cursor = conn.cursor()

pygame.init()
pygame.font.init()

# --- LOGIN LOOP ---
# On lance le launcher avant d'ouvrir la fenêtre principale du jeu
connected = run_launcher()
if not connected:
    pygame.quit()
    sys.exit()

# Configuration de l'écran après login
screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
pygame.display.set_caption("Ludo Game")

# Grid configuration
ROWS, COLS = 15, 15
CELL_WIDTH, CELL_HEIGHT = 50, 50
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}
COLOR_TO_PYGAME_COLOR = {"red": RED, "blue": BLUE, "yellow": YELLOW, "green": GREEN}

# Initialize grid
grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)
color_ludo(grid)
storage_cells = setup_home_and_storage(grid, colors)
game_path_length = setup_game_path(grid)

# Game initialization
players = [Player("Player 1", 1), Player("Player 2", 2), Player("Player 3", 3), Player("Player 4", 4)]
game = Game(players, grid, game_path_length)
dice = Dice()
font_dice = pygame.font.Font(None, 120)  # Police plus grande pour le dé
font_ui = pygame.font.SysFont("Segoe UI", 16)

# UI layout constants
SIDEBAR_W = 300
HEADER_H = 64
BOARD_LEFT = 40
BOARD_TOP = HEADER_H + 20
clock = pygame.time.Clock()
FPS = 60


# --- Fonctions de dessin ---

def draw_gradient_background(surface):
    h = surface.get_height()
    top_color, bottom_color = (30, 30, 40), (12, 12, 20)
    for i in range(h):
        t = i / h
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, i), (surface.get_width(), i))


def draw_header(surface):
    header_rect = pygame.Rect(0, 0, surface.get_width(), HEADER_H)
    pygame.draw.rect(surface, (20, 20, 30), header_rect)
    title_font = pygame.font.SysFont("Segoe UI", 24, bold=True)
    text = title_font.render("Ludo Game", True, WHITE)
    surface.blit(text, (20, HEADER_H // 2 - text.get_height() // 2))


def draw_sidebar(surface):
    w = SIDEBAR_W
    rect = pygame.Rect(surface.get_width() - w, HEADER_H, w, surface.get_height() - HEADER_H)
    pygame.draw.rect(surface, (14, 14, 18), rect, border_radius=12)
    inner = rect.inflate(-18, -18)
    pygame.draw.rect(surface, (22, 22, 26), inner, border_radius=10)

    # Info Joueur Actif
    curr_p = game.players[game.current_player_index]
    p_text = font_ui.render(f"Active player: {curr_p.name}", True, WHITE)
    surface.blit(p_text, (inner.left + 12, inner.top + 40))

    # Indicateur couleur
    color_rect = pygame.Rect(inner.left + 12, inner.top + 65, 40, 10)
    pygame.draw.rect(surface, COLOR_TO_PYGAME_COLOR.get(curr_p.color), color_rect, border_radius=4)

    # Bouton Dé
    btn = pygame.Rect(inner.left + 12, inner.top + 100, inner.width - 24, 45)
    btn_color = (200, 200, 200) if game.rolled_dice is None else (100, 100, 100)
    pygame.draw.rect(surface, btn_color, btn, border_radius=8)
    txt_btn = font_ui.render("LANCER LE DÉ" if not dice.animating else "ROLLING...", True, BLACK)
    surface.blit(txt_btn, (btn.centerx - txt_btn.get_width() // 2, btn.centery - txt_btn.get_height() // 2))

    # Message de statut
    msg_wrapped = font_ui.render(game.message, True, (200, 200, 100))
    surface.blit(msg_wrapped, (inner.left + 12, inner.top + 250))

    return btn


def draw_pawns(surface, grid, offset_x, offset_y, cell_w, cell_h):
    pawn_radius = cell_w // 3
    for player in game.players:
        for pawn in player.pawns:
            if pawn.is_finished: continue

            # Position sur le plateau
            if pawn.position is not None:
                cell_info = game.get_cell_by_position(pawn.position)
                if cell_info:
                    c_row, c_col = cell_info['row'], cell_info['col']
                    cx = offset_x + c_col * cell_w + cell_w // 2
                    cy = offset_y + c_row * cell_h + cell_h // 2

                    pygame.draw.circle(surface, COLOR_TO_PYGAME_COLOR[player.color], (cx, cy), pawn_radius)
                    pygame.draw.circle(surface, BLACK, (cx, cy), pawn_radius, 2)

            # Position en storage
            else:
                s_info = storage_cells.get((player.color, pawn.pawn_id))
                if s_info:
                    cx = offset_x + s_info['col'] * cell_w + cell_w // 2
                    cy = offset_y + s_info['row'] * cell_h + cell_h // 2
                    pygame.draw.circle(surface, COLOR_TO_PYGAME_COLOR[player.color], (cx, cy), pawn_radius - 5)
                    pygame.draw.circle(surface, BLACK, (cx, cy), pawn_radius - 5, 1)


def handle_pawn_click(row, col):
    if game.rolled_dice is None:
        game.set_message("Roll the dice first!")
        return

    # La logique est déjà dans votre game.py via handle_pawn_click
    # Appeler la fonction fournie dans votre script initial
    # (Note: Assurez-vous que handle_pawn_click est accessible ou incluse)
    pass

def world_to_cell(mx, my, left, top, cw, ch):
    """Convertit les coordonnées de la souris (pixels) en index de grille (ligne, colonne)"""
    col = (mx - left) // cw
    row = (my - top) // ch
    return int(row), int(col)

# ================= MAIN LOOP =================
run = True
roll_button_rect = pygame.Rect(0, 0, 0, 0)

while run:
    # 1. Gestion des entrées
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clic sur le bouton de dé
            if roll_button_rect.collidepoint(mx, my):
                if not dice.animating and game.rolled_dice is None:
                    dice.start_animation()

            # Clic sur une case du plateau
            r, c = world_to_cell(mx, my, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)
            if 0 <= r < ROWS and 0 <= c < COLS:
                if game.rolled_dice is not None and not dice.animating:
                    # On utilise la fonction handle_pawn_click définie plus haut
                    player = game.players[game.current_player_index]
                    cell = grid[r][c]

                    # Logique simplifiée intégrée ici pour le main
                    if cell.cell_type == STORAGE:
                        pawn = next((p for p in player.pawns if
                                     p.position is None and storage_cells.get((player.color, p.pawn_id))['row'] == r),
                                    None)
                        if pawn and game.try_to_release_pawn(pawn, game.rolled_dice):
                            game.post_move_cleanup()
                    elif cell.id is not None:
                        pawns = game.get_pawns_on_cell(r, c)
                        pawn = next((p for p in pawns if p.player == player), None)
                        if pawn and game.try_to_move_pawn(pawn, game.rolled_dice):
                            game.post_move_cleanup()

    # 2. Mises à jour (Logic)
    dice.update()
    if not dice.animating and dice.result is not None and game.rolled_dice is None:
        game.rolled_dice = dice.result
        game.set_message(f"Rolled a {game.rolled_dice}! Select a pawn.")
        dice.result = None

    # 3. Dessin (Render)
    draw_gradient_background(screen)
    draw_header(screen)
    roll_button_rect = draw_sidebar(screen)

    # Plateau
    board_w, board_h = COLS * CELL_WIDTH, ROWS * CELL_HEIGHT
    pygame.draw.rect(screen, (30, 30, 36), (BOARD_LEFT - 5, BOARD_TOP - 5, board_w + 10, board_h + 10),
                     border_radius=10)

    for row_cells in grid:
        for cell in row_cells:
            cell.draw(screen, BOARD_LEFT, BOARD_TOP)

    # Highlights
    hr, hc = world_to_cell(mx, my, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)
    if 0 <= hr < ROWS and 0 <= hc < COLS:
        pygame.draw.rect(screen, (255, 255, 255),
                         (BOARD_LEFT + hc * CELL_WIDTH, BOARD_TOP + hr * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2)

    draw_pawns(screen, grid, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)

    # Affichage du dé visuel
    dice_x = roll_button_rect.centerx - 40
    dice_y = roll_button_rect.bottom + 50
    # On dessine un rectangle pour le dé
    pygame.draw.rect(screen, WHITE, (dice_x, dice_y, 80, 80), border_radius=10)
    res_txt = font_dice.render(str(dice.current_display), True, BLACK)
    screen.blit(res_txt, (dice_x + 40 - res_txt.get_width() // 2, dice_y + 40 - res_txt.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()