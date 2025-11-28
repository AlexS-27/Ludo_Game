import pygame
import sys

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((1400, 800)
                                 #,pygame.RESIZABLE
) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("LudoGame Launcher")

# --- Colors & Fonts ---
BACKGROUND_GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (100, 100, 100)
ACTIVE_BORDER = (0, 100, 255)  # Blue border when typing
INACTIVE_BORDER = (200, 200, 200)  # Light border when not active

FONT_TITLE = pygame.font.SysFont("Arial", 60, bold=True)
FONT_LABEL = pygame.font.SysFont("Arial", 24)
FONT_INPUT = pygame.font.SysFont("Arial", 28)


# --- Class: Button ---
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = WHITE
        self.hover_color = (230, 230, 230)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        # Draw button background
        curr_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, curr_color, self.rect)

        # Draw Text
        text_surf = FONT_LABEL.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


# --- Class: InputBox ---
class InputBox:
    def __init__(self, x, y, width, height, is_password=False, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = INACTIVE_BORDER
        self.text = ""
        self.is_password = is_password
        self.active = False
        self.placeholder = placeholder

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active if user clicked on the box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = ACTIVE_BORDER if self.active else INACTIVE_BORDER

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"Input Submitted: {self.text}")  # Optional: Action on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add unicode character
                self.text += event.unicode

    def draw(self, surface):
        # Draw background of input box (White)
        pygame.draw.rect(surface, WHITE, self.rect)

        # Render text (Mask it if it is a password) (With help of AI to hide password)
        display_text = "*" * len(self.text) if self.is_password else self.text

        # Render the text surface
        txt_surface = FONT_INPUT.render(display_text, True, BLACK)

        # Vertical centering
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

        # Draw the border (Blue if active, Grey if not)
        pygame.draw.rect(surface, self.color, self.rect, 2)


# --- State Management ---
current_state = "MENU"  # Can be MENU, NEW_GAME, LOAD_GAME


# --- Callback Functions ---
def switch_to_new_game():
    global current_state
    current_state = "NEW_GAME"


def switch_to_load_game():
    global current_state
    current_state = "LOAD_GAME"


def switch_to_menu():
    global current_state
    current_state = "MENU"


def action_create():
    print("--- Creating Game ---")
    print(f"Name: {input_newgame_name.text}")
    #print(f"Pass: {input_ng_pass.text}")
    print(f"Players: {input_newgame_players.text}")
    # Here you would add the code to actually start the game logic


def action_load():
    print("--- Loading Game ---")
    print(f"Name: {input_loadgame_name.text}")
    #print(f"Pass: {input_loadgame_pass.text}")


# --- Widget Instantiation ---

# 1. MENU SCREEN WIDGETS
btn_menu_newgame = Button(600, 500, 200, 50, "Start a new game", switch_to_new_game)
btn_menu_loadgame = Button(600, 600, 200, 50, "Load an existing game", switch_to_load_game)

# 2. NEW GAME SCREEN WIDGETS
input_newgame_name = InputBox(500, 300, 400, 50)
input_newgame_pass = InputBox(500, 420, 400, 50, is_password=True)
input_newgame_players = InputBox(600, 540, 200, 50)  # Smaller box for numbers
btn_create_confirm = Button(600, 650, 200, 50, "Create a new game", action_create)

# 3. LOAD GAME SCREEN WIDGETS
input_loadgame_name = InputBox(500, 320, 400, 50)
input_loadgame_pass = InputBox(500, 440, 400, 50, is_password=True)
btn_load_confirm = Button(600, 600, 200, 50, "Load the game", action_load)

# Global Back Button (optional, to get back to menu during testing)
btn_back = Button(50, 50, 100, 40, "< Back", switch_to_menu)


# --- Drawing Helpers ---
def draw_text_centered(text, font, y_pos, color=BLACK):
    s = font.render(text, True, color)
    rect = s.get_rect(center=(screen_width // 2, y_pos))
    screen.blit(s, rect)


# --- Main Loop ---
running = True
while running:
    screen.fill(BACKGROUND_GREY)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Handle Back Button everywhere except Main Menu
        if current_state != "MENU":
            btn_back.handle_event(event)

        # State-Specific Event Handling
        if current_state == "MENU":
            btn_menu_newgame.handle_event(event)
            btn_menu_loadgame.handle_event(event)

        elif current_state == "NEW_GAME":
            input_newgame_name.handle_event(event)
            input_newgame_pass.handle_event(event)
            input_newgame_players.handle_event(event)
            btn_create_confirm.handle_event(event)

        elif current_state == "LOAD_GAME":
            input_loadgame_name.handle_event(event)
            input_loadgame_pass.handle_event(event)
            btn_load_confirm.handle_event(event)

    # --- Drawing ---
    if current_state == "MENU":
        draw_text_centered("Welcome to", FONT_TITLE, 250)
        draw_text_centered("LudoGame!", FONT_TITLE, 320)
        btn_menu_newgame.draw(screen)
        btn_menu_loadgame.draw(screen)

    elif current_state == "NEW_GAME":
        btn_back.draw(screen)  # Helper to go back

        draw_text_centered("Please give your game a name :", FONT_LABEL, 270)
        input_newgame_name.draw(screen)

        draw_text_centered("Please give your game a password :", FONT_LABEL, 390)
        input_newgame_pass.draw(screen)

        draw_text_centered("How many players will compete ?", FONT_LABEL, 510)
        input_newgame_players.draw(screen)

        btn_create_confirm.draw(screen)

    elif current_state == "LOAD_GAME":
        btn_back.draw(screen)  # Helper to go back

        draw_text_centered("Please enter the game's name :", FONT_LABEL, 290)
        input_loadgame_name.draw(screen)

        draw_text_centered("Please enter the game's password :", FONT_LABEL, 410)
        input_loadgame_pass.draw(screen)

        btn_load_confirm.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
