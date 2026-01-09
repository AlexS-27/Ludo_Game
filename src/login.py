"""
Ludo Game - Launcher & Login Module
Description: Manages the pre-game interface, including state management for 
             creating new games or loading existing ones from the database.
Authors: Alexandre Ramirez, Kilian Testard, Niels Delafontaine et Alex Kamano with help of IA
Date: 2025
"""

import pygame
import sys
import traceback
from src.linkwithdatabase import LoadGameDB, CreateNewGameDB

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((1400, 800))
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Ludo Game Launcher")

# --- UI Constants: Colors ---
BACKGROUND_GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (100, 100, 100)
ACTIVE_BORDER = (0, 100, 255)  # Blue highlight for active input
INACTIVE_BORDER = (200, 200, 200)  # Grey border for inactive input

# --- UI Constants: Typography ---
FONT_TITLE = pygame.font.SysFont("Arial", 60, bold=True)
FONT_LABEL = pygame.font.SysFont("Arial", 24)
FONT_INPUT = pygame.font.SysFont("Arial", 28)


def run_launcher():
    """
    Executes the launcher loop. 
    Handles the menu navigation, database calls, and input validation.
    Returns: bool (True when a successful session starts).
    """

    class Button:
        """Interactive UI button component."""

        def __init__(self, x, y, width, height, text, callback):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.callback = callback
            self.color = WHITE
            self.hover_color = (230, 230, 230)

        def draw(self, surface):
            """Renders the button with hover effect detection."""
            mouse_pos = pygame.mouse.get_pos()
            curr_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
            pygame.draw.rect(surface, curr_color, self.rect)

            text_surf = FONT_LABEL.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

        def handle_event(self, event):
            """Processes mouse click events for the button."""
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    try:
                        self.callback()
                    except Exception:
                        print("Exception in button callback:")
                        traceback.print_exc()

    class InputBox:
        """Text input field for user data entry."""

        def __init__(self, x, y, width, height, is_password=False, placeholder=""):
            self.rect = pygame.Rect(x, y, width, height)
            self.color = INACTIVE_BORDER
            self.text = ""
            self.is_password = is_password
            self.active = False
            self.placeholder = placeholder

        def handle_event(self, event):
            """Manages focus toggling and keyboard input."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle focus based on collision
                self.active = self.rect.collidepoint(event.pos)
                self.color = ACTIVE_BORDER if self.active else INACTIVE_BORDER

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode:
                    self.text += event.unicode

        def draw(self, surface):
            """Renders the input field and typed text (with password masking)."""
            pygame.draw.rect(surface, WHITE, self.rect)

            # Mask characters for password security
            display_text = "*" * len(self.text) if self.is_password else self.text
            txt_surface = FONT_INPUT.render(display_text, True, BLACK)

            surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))
            pygame.draw.rect(surface, self.color, self.rect, 2)

    # --- Launcher State ---
    current_state = "MENU"  # Possible states: MENU, NEW_GAME, LOAD_GAME

    # --- Navigation Logic ---
    def switch_to_new_game():
        nonlocal current_state
        current_state = "NEW_GAME"

    def switch_to_load_game():
        nonlocal current_state
        current_state = "LOAD_GAME"

    def switch_to_menu():
        nonlocal current_state
        current_state = "MENU"

    # --- Data Processing Logic ---
    def action_create():
        """Validates input and creates a new game entry in the database."""
        nbr_player_text = input_newgame_players.text.strip()

        # Default to 1 player if empty, otherwise attempt conversion
        try:
            nbr_player = int(nbr_player_text) if nbr_player_text else 1
        except ValueError:
            print("Invalid player count: Please enter an integer between 1 and 4.")
            return False

        # Enforce player range (1-4)
        if nbr_player < 1 or nbr_player > 4:
            print("Player count must be between 1 and 4.")
            return False

        print(f"Creating Game - Name: {input_newgame_name.text}, Players: {nbr_player}")
        try:
            success = CreateNewGameDB(input_newgame_name.text, input_newgame_pass.text)
            if success:
                nonlocal running
                running = False
                return True
            else:
                print("Creation failed: Name may already be taken.")
        except Exception:
            traceback.print_exc()

    def action_load():
        """Attempts to authenticate and load an existing game from the database."""
        print(f"Attempting to load: {input_loadgame_name.text}")
        try:
            data = LoadGameDB(input_loadgame_name.text, input_loadgame_pass.text)
            if data:
                nonlocal running
                running = False
                return True
            else:
                print("Load failed: Incorrect credentials or game not found.")
        except Exception:
            traceback.print_exc()

    # --- Component Instantiation ---
    btn_menu_newgame = Button(600, 500, 200, 50, "Start New Game", switch_to_new_game)
    btn_menu_loadgame = Button(600, 600, 200, 50, "Load Saved Game", switch_to_load_game)

    input_newgame_name = InputBox(500, 300, 400, 50)
    input_newgame_pass = InputBox(500, 420, 400, 50, is_password=True)
    input_newgame_players = InputBox(600, 540, 200, 50)
    btn_create_confirm = Button(600, 650, 200, 50, "Create Game", action_create)

    input_loadgame_name = InputBox(500, 320, 400, 50)
    input_loadgame_pass = InputBox(500, 440, 400, 50, is_password=True)
    btn_load_confirm = Button(600, 600, 200, 50, "Login & Load", action_load)

    btn_back = Button(50, 50, 100, 40, "< Back", switch_to_menu)

    def draw_text_centered(text, font, y_pos, color=BLACK):
        """Helper to render horizontally centered text on the screen."""
        s = font.render(text, True, color)
        rect = s.get_rect(center=(screen_width // 2, y_pos))
        screen.blit(s, rect)

    # --- Main Launcher Loop ---
    clock = pygame.time.Clock()
    running = True

    try:
        while running:
            screen.fill(BACKGROUND_GREY)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                # Input handling based on current screen state
                if current_state != "MENU":
                    btn_back.handle_event(event)

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

            # --- Rendering Phase ---
            if current_state == "MENU":
                draw_text_centered("Welcome to", FONT_TITLE, 250)
                draw_text_centered("LudoGame!", FONT_TITLE, 320)
                btn_menu_newgame.draw(screen)
                btn_menu_loadgame.draw(screen)

            elif current_state == "NEW_GAME":
                btn_back.draw(screen)
                draw_text_centered("Enter a game name:", FONT_LABEL, 270)
                input_newgame_name.draw(screen)
                draw_text_centered("Enter a password:", FONT_LABEL, 390)
                input_newgame_pass.draw(screen)
                draw_text_centered("Number of players (1-4):", FONT_LABEL, 510)
                input_newgame_players.draw(screen)
                btn_create_confirm.draw(screen)

            elif current_state == "LOAD_GAME":
                btn_back.draw(screen)
                draw_text_centered("Game Name:", FONT_LABEL, 290)
                input_loadgame_name.draw(screen)
                draw_text_centered("Password:", FONT_LABEL, 410)
                input_loadgame_pass.draw(screen)
                btn_load_confirm.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    except Exception:
        traceback.print_exc()
    finally:
        return True


if __name__ == "__main__":
    run_launcher()