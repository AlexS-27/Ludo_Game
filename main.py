import pygame
from src.grid_and_board.cell import RED, GREEN, BLUE, YELLOW, WHITE, BLACK, Cell, BORDER
from src.grid_and_board.board import color_ludo
from src.grid_and_board.arrows import draw_wide_arrow
from src.grid_and_board.grid_setup import create_grid, setup_home_and_storage, setup_game_path

pygame.init()
pygame.font.init()

# setup pygame
screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()
#setup window's title
pygame.display.set_caption("Ludo Game")

# Grid
ROWS, COLS = 15, 15
CELL_WIDTH, CELL_HEIGHT = 50, 50
colors = {"RED": RED, "BLUE": BLUE, "YELLOW": YELLOW, "GREEN": GREEN}

# create grid & layout
grid = create_grid(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)
color_ludo(grid)
setup_home_and_storage(grid, colors)
setup_game_path(grid)

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
    sf = pygame.font.SysFont("Segoe UI", 14)
    surface.blit(sf.render("Joueur actif: Rouge", True, (200, 200, 200)), (inner.left + 12, inner.top + 44))
    # button placeholder
    btn = pygame.Rect(inner.left + 12, inner.top + 80, inner.width - 24, 40)
    pygame.draw.rect(surface, (255, 255, 255), btn, border_radius=8)
    pygame.draw.rect(surface, (12, 12, 12), btn, 2, border_radius=8)
    surface.blit(sf.render("Lancer le dé", True, (12, 12, 12)), (btn.left + 16, btn.top + 8))

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

# main loop
run = True
while run:
    dt = clock.tick(FPS) / 1000.0
    pulse_t += dt

    events = pygame.event.get()
    for event in events:
        #quit pygame
        if event.type == pygame.QUIT:
            run = False
        #React to resize
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        #Cliquer : Montre l'id de la case -Alex
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # translate coords to board-local
            row, col = world_to_cell(mx, my, BOARD_LEFT, BOARD_TOP, CELL_WIDTH, CELL_HEIGHT)
            if 0 <= row < ROWS and 0 <= col < COLS:
                clicked_cell = grid[row][col]
                print(f"Case cliquée: ID={clicked_cell.id}, Type={clicked_cell.cell_type}, RowCol=({row},{col})")

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
        rect = pygame.Rect(BOARD_LEFT + hover_cell.col * CELL_WIDTH, BOARD_TOP + hover_cell.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 28))
        pygame.draw.rect(s, (255, 255, 255, 18), s.get_rect(), border_radius=8)
        screen.blit(s, rect.topleft)

    if clicked_cell:
        rect = pygame.Rect(BOARD_LEFT + clicked_cell.col * CELL_WIDTH, BOARD_TOP + clicked_cell.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
    #Draw arrow
    #Red arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3,
                    end_row=7, end_col=7, color=RED,
                    cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="down",
                    offset_x=BOARD_LEFT, offset_y=BOARD_TOP)
    #Green arrow
    draw_wide_arrow(screen, start_row=6, start_col=6, base_width=3,
                    end_row=7, end_col=7, color=GREEN,
                    cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="right",
                    offset_x=BOARD_LEFT, offset_y=BOARD_TOP)
    #Yellow arrow
    draw_wide_arrow(screen, start_row=8, start_col=6, base_width=3,
                    end_row=7, end_col=7, color=YELLOW,
                    cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="up",
                    offset_x=BOARD_LEFT, offset_y=BOARD_TOP)
    #Blue arrow
    draw_wide_arrow(screen, start_row=6, start_col=8, base_width=3,
                    end_row=7, end_col=7, color=BLUE,
                    cell_width=CELL_WIDTH, cell_height=CELL_HEIGHT,
                    direction="left",
                    offset_x=BOARD_LEFT, offset_y=BOARD_TOP)

    pygame.display.flip()

pygame.quit()
