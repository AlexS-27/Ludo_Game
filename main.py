# main.py
import pygame
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, WHITE, BLACK, Cell, BORDER, STORAGE, HOME_AREA, NORMAL_HORIZONTAL, NORMAL_VERTICAL, SAFE_PATH
from src.grid_and_board.board import color_ludo
from src.grid_and_board.arrows import draw_entry_arrows
from src.grid_and_board.grid_setup import create_grid, setup_home_and_storage, setup_game_path
from src.dice_roll import Dice
from src.game import Game
from src.player import Player

pygame.init()
pygame.font.init()

# setup pygame
screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()
#setup window's title
pygame.display.set_caption("Ludo Game")

# Grid configuration
ROWS, COLS = 15, 15
CELL_WIDTH, CELL_HEIGHT = 50, 50
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}
COLOR_TO_PYGAME_COLOR = {"red": RED, "blue": BLUE, "yellow": YELLOW, "green": GREEN}

# Initialize grid
grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)
# Apply coloring (board.py)
color_ludo(grid)
# Setup home areas and storage cells
storage_cells = setup_home_and_storage(grid, colors)
# Setup paths
game_path_length = setup_game_path(grid)

# game initialization
players = [Player("Player 1", 1),
           Player("Player 2", 2),
           Player("Player 3", 3),
           Player("Player 4", 4)]
game = Game(players, grid, game_path_length)
dice = Dice()
font = pygame.font.Font(None, 80)

# UI layout constants
SIDEBAR_W = 300
HEADER_H = 64
BOARD_LEFT = 40
BOARD_TOP = HEADER_H + 20

# Clock for animations
clock = pygame.time.Clock()
FPS = 60

# For hover and click highlights
hover_cell = None
clicked_cell = None

# Simple pulse timer for arrow animation
pulse_t = 0.0

# reference for the dice button in the sidebar
dice_btn_rect = None

def draw_gradient_background(surface, top_color=(30, 30, 40), bottom_color=(12, 12, 20)):
    """Vertical gradient background"""
    h = surface.get_height()
    for i in range(h):
        t = i / h
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, i), (surface.get_width(), i))

def draw_header(surface, title="Ludo Game"):
    header_rect = pygame.Rect(0, 0, surface.get_width(), HEADER_H)
    # header background
    pygame.draw.rect(surface, (20, 20, 30), header_rect)
    # title
    font = pygame.font.SysFont("Segoe UI", 24, bold=True)
    text = font.render(title, True, WHITE)
    surface.blit(text, (20, HEADER_H//2 - text.get_height()//2))
    # small subtitle
    subf = pygame.font.SysFont("Segoe UI", 14)
    sub = subf.render("Prototype — UI améliorée", True, (180, 180, 190))
    surface.blit(sub, (20 + text.get_width() + 16, HEADER_H//2 - sub.get_height()//2))

def draw_sidebar(surface):
    global dice_btn_rect
    w = SIDEBAR_W
    rect = pygame.Rect(surface.get_width() - w, HEADER_H, w, surface.get_height() - HEADER_H)

    # panel background
    pygame.draw.rect(surface, (14, 14, 18), rect, border_radius=12)

    # inner card
    inner = rect.inflate(-18, -18)
    pygame.draw.rect(surface, (22, 22, 26), inner, border_radius=10)

    # content: title + placeholders
    f = pygame.font.SysFont("Segoe UI", 18, bold=True)
    t = f.render("Game Panel", True, WHITE)
    surface.blit(t, (inner.left + 12, inner.top + 12))

    # displaying active player
    current_player_name = game.players[game.current_player_index].name
    current_player_color = game.players[game.current_player_index].color

    sf = pygame.font.SysFont("Segoe UI", 14)
    player_text = sf.render(f"Active player: {current_player_name}", True, (200, 200, 200))
    surface.blit(player_text, (inner.left + 12, inner.top + 44))

    # color indicator
    color_rect = pygame.Rect(inner.left + 12 + player_text.get_width() + 8, inner.top + 44, 16, 16)
    pygame.draw.rect(surface, COLOR_TO_PYGAME_COLOR.get(current_player_color, WHITE), color_rect, border_radius=4)
    pygame.draw.rect(surface, BLACK, color_rect, 1, border_radius=4)

    # dice button
    btn = pygame.Rect(inner.left + 12, inner.top + 80, inner.width - 24, 40)
    dice_btn_rect = btn  # Stocker pour la gestion du clic

    button_color = (200, 200, 200) if not dice.animating and game.rolled_dice is None else (100, 100, 100)
    text_color = BLACK if not dice.animating and game.rolled_dice is None else (50, 50, 50)

    pygame.draw.rect(surface, button_color, btn, border_radius=8)
    pygame.draw.rect(surface, (12, 12, 12), btn, 2, border_radius=8)

    btn_text = "Roll the dice"
    if dice.animating:
        btn_text = "rolling..."
    elif game.rolled_dice is not None:
        btn_text = f"Dice: {game.rolled_dice} - Select a pawn"

    t_btn = sf.render(btn_text, True, text_color)
    surface.blit(t_btn, (btn.left + btn.width // 2 - t_btn.get_width() // 2, btn.top + 8))

    # displaying the dice roll
    if game.rolled_dice is not None and not dice.animating:
        df = pygame.font.SysFont("Segoe UI", 48, bold=True)
        dt = df.render(str(game.rolled_dice), True, WHITE)
        surface.blit(dt, (inner.left + inner.width // 2 - dt.get_width() // 2, inner.top + 150))

    # displaying status
    if game.message:
        msg_f = pygame.font.SysFont("Segoe UI", 16)
        msg_t = msg_f.render(game.message, True, YELLOW)
        surface.blit(msg_t, (inner.left + 12, inner.top + 220))


def draw_board_background(surface, left, top, cols, rows, cell_w, cell_h):
    # subtle shadow panel
    board_w = cols * cell_w
    board_h = rows * cell_h
    panel = pygame.Rect(left - 12, top - 12, board_w + 24, board_h + 24)
    shadow = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=18)
    surface.blit(shadow, (panel.left + 6, panel.top + 6))
    pygame.draw.rect(surface, (30, 30, 36), panel, border_radius=18)

def world_to_cell(mx, my, left, top, cw, ch):
    col = (mx - left) // cw
    row = (my - top) // ch
    return int(row), int(col)

# with AI
def draw_pawns(surface, grid, offset_x, offset_y, cell_w, cell_h):
    pawn_radius = cell_w // 4

    for player in game.players:
        for pawn in player.pawns:
            if pawn.position is not None and not pawn.is_finished:
                cell_info = game.get_cell_by_position(pawn.position)
                if cell_info is None:
                    continue

                cell = cell_info['cell']

                # cell center coordinates
                center_x = offset_x + cell.col * cell_w + cell_w // 2
                center_y = offset_y + cell.row * cell_h + cell_h // 2

                # check if multiple pawns are on the same cell
                pawns_on_cell = game.get_pawns_on_cell(cell.row, cell.col)
                num_pawns = len(pawns_on_cell)

                # to be implemented later: drawing multiple pawns next to each other
                pawn_color = COLOR_TO_PYGAME_COLOR.get(player.color)

                pygame.draw.circle(surface, pawn_color, (center_x, center_y), pawn_radius)
                pygame.draw.circle(surface, BLACK, (center_x, center_y), pawn_radius, 1)

            elif pawn.position is None and not pawn.is_finished:
                # the pawn is in storage
                storage_cell_info = storage_cells.get((player.color, pawn.pawn_id))
                if storage_cell_info:
                    r, c = storage_cell_info['row'], storage_cell_info['col']
                    cell = grid[r][c]
                    center_x = offset_x + cell.col * cell_w + cell_w // 2
                    center_y = offset_y + cell.row * cell_h + cell_h // 2

                    pawn_color = COLOR_TO_PYGAME_COLOR.get(player.color)

                    storage_index = pawn.pawn_id

                    offsets = [(-pawn_radius, -pawn_radius), (pawn_radius, -pawn_radius),
                               (-pawn_radius, pawn_radius), (pawn_radius, pawn_radius)]

                    dx, dy = offsets[storage_index]

                    pygame.draw.circle(surface, pawn_color, (center_x + dx // 2, center_y + dy // 2), pawn_radius - 2)
                    pygame.draw.circle(surface, BLACK, (center_x + dx // 2, center_y + dy // 2), pawn_radius - 2, 1)


# with AI
def handle_pawn_click(row, col):
    if game.rolled_dice is None:
        game.set_message("Please roll the dice first.")
        return

    player = game.players[game.current_player_index]
    cell = grid[row][col]
    if cell.cell_type == STORAGE:
        pawn_to_move = next((p for p in player.pawns
                             if p.position is None and
                             not p.is_finished and
                             storage_cells.get((player.color, p.pawn_id), {}).get('row') == row and
                             storage_cells.get((player.color, p.pawn_id), {}).get('col') == col), None)
        if pawn_to_move:
            if game.try_to_release_pawn(pawn_to_move, game.rolled_dice):
                game.post_move_cleanup()
            else:
                game.set_message(f"You need a 5 to get the pawn out of storage, not a {game.rolled_dice}")
        else:
            game.set_message("This is not your in-storage pawn.")

    elif cell.id is not None and cell.cell_type not in [HOME_AREA]:
        pawns_on_cell = game.get_pawns_on_cell(row, col)
        pawn_to_move = next((p for p in pawns_on_cell if p.player.color == player.color), None)
        if pawn_to_move:
            if game.try_to_move_pawn(pawn_to_move, game.rolled_dice):
                game.post_move_cleanup()
            else:
                game.set_message("None of your pawns on this cell are playable.")
        else:
            game.set_message("Non-playble cell, or no pawn to select.")


# Main loop
run = True

while run:

    dice.update()

    dt = clock.tick(FPS) / 1000.0
    pulse_t += dt

    # Event handling
    events = pygame.event.get()
    for event in events:
        # quit pygame
        if event.type == pygame.QUIT:
            run = False
        # React to resize
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Click on the dice button
            if dice_btn_rect and dice_btn_rect.collidepoint(mx, my):
                if not dice.animating and game.rolled_dice is None:
                    # Roll the dice, begin animation
                    dice.start_animation()
                    game.set_message("Dice rolled !")
                    # Result will be updated in dice.update() and fetched here after the animation
                elif game.rolled_dice is not None:
                    # If the dice was already rolled, then the button is useless. Wait on pawn select click.
                    game.set_message("Select a pwan to move.")

            # Click on the board
            row, col = world_to_cell(mx, my, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)
            if 0 <= row < ROWS and 0 <= col < COLS:
                clicked_cell = grid[row][col]
                # print(f"Cell clicked: ID={clicked_cell.id}, Type={clicked_cell.cell_type}, RowCol=({row},{col})")

                # If the dice was rolled, try to move a pawn
                if game.rolled_dice is not None and not dice.animating:
                    handle_pawn_click(row, col)

    # After the dice finished the animation, update the result in-game
    if not dice.animating and dice.result is not None and game.rolled_dice is None:
        game.rolled_dice = dice.result
        game.set_message(f"Dice roll: {game.rolled_dice}. Select a pawn.")
        # Reset dice object for next turn
        dice.result = None

    # hover tracking
    mx, my = pygame.mouse.get_pos()
    hr, hc = world_to_cell(mx, my, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)
    if 0 <= hr < ROWS and 0 <= hc < COLS:
        hover_cell = grid[hr][hc]
    else:
        hover_cell = None

    # draw background & UI
    draw_gradient_background(screen)
    draw_header(screen)
    draw_sidebar(screen)
    draw_board_background(screen, BOARD_LEFT, BOARD_TOP, COLS, ROWS, CELL_WIDTH, CELL_HEIGHT)

    # draw cells
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            # temporarily offset the cell drawing by BOARD_LEFT/BOARD_TOP
            # so we translate cell.draw to use the board origin
            cell.draw(screen, x_offset=BOARD_LEFT, y_offset=BOARD_TOP)

    # highlights
    if hover_cell:
        # draw light overlay on hover
        rect = pygame.Rect(BOARD_LEFT + hover_cell.col * CELL_WIDTH, BOARD_TOP + hover_cell.row * CELL_HEIGHT,
                           CELL_WIDTH, CELL_HEIGHT)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 28))
        pygame.draw.rect(s, (255, 255, 255, 18), s.get_rect(), border_radius=8)
        screen.blit(s, rect.topleft)

    if clicked_cell:
        rect = pygame.Rect(BOARD_LEFT + clicked_cell.col * CELL_WIDTH, BOARD_TOP + clicked_cell.row * CELL_HEIGHT,
                           CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)

    # Draw pawns
    draw_pawns(screen, grid, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)

    # Draw arrow (une seule pour l'exemple)
    draw_entry_arrows(
        screen,
        start_row=6, start_col=6, base_width=3,
        end_row=7, end_col=7, color=RED,
        cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
        direction="down",
        offset_x=BOARD_LEFT, offset_y=BOARD_TOP
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
