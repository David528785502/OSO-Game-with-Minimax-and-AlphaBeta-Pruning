import pygame
import json
import os

class ScreenMenu:
    def __init__(self, resolution, opponent, board_size, language, manager):
        self.resolution = resolution
        self.opponent = opponent
        self.board_size = board_size
        self.language = language
        self.manager = manager

        # Background
        self.background_x = 0
        self.background_speed = 1
        self.background = pygame.image.load("assets/images/background.png")

        # Logo
        base_dir = os.path.dirname(__file__)
        logo_path = os.path.join(base_dir, "..", "assets", "images", "logo.png")
        self.logo = pygame.image.load(logo_path)

        # Languages
        lang_path = os.path.join(base_dir, "..", "languages", "languages.json")
        with open(lang_path, "r", encoding="utf-8") as f:
            self.LANGUAGES = json.load(f)

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        lang_data = self.LANGUAGES.get(self.language, self.LANGUAGES["en"])
        self.lang_data = lang_data

        button_width = int(self.resolution[0] * 0.35)
        button_height = int(self.resolution[1] * 0.12)
        button_x = (self.resolution[0] - button_width) // 2
        space_between_buttons_pct = 0.02

        first_button_y = int(self.resolution[1] * 0.55)
        self.buttons = [
            (lang_data["play"], pygame.Rect(button_x, first_button_y, button_width, button_height)),
            (lang_data["options"], pygame.Rect(
                button_x, first_button_y + button_height + int(self.resolution[1] * space_between_buttons_pct),
                button_width, button_height)),
            (lang_data["exit"], pygame.Rect(
                button_x, first_button_y + 2 * (button_height + int(self.resolution[1] * space_between_buttons_pct)),
                button_width, button_height))
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (_, rect) in enumerate(self.buttons):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            from screens.screen_game import ScreenGame
                            self.manager.set_screen(ScreenGame(self.resolution, self.opponent, self.board_size, self.language, self.manager))
                        elif i == 1:
                            from screens.screen_options import ScreenOptions
                            self.manager.set_screen(ScreenOptions(self.resolution, self.opponent, self.board_size, self.language, self.manager))
                        elif i == 2:
                            pygame.quit()
                            quit()

    def update(self):
        self.background_x -= self.background_speed
        if self.background_x <= -self.background.get_width():
            self.background_x = 0

    def draw(self, screen):
        # Background scroll
        screen.blit(self.background, (self.background_x, -1))
        screen.blit(self.background, (self.background_x + self.background.get_width(), -1))

        # Logo
        logo_width = int(self.resolution[0] * 0.30)
        logo_height = int(self.resolution[1] * 0.40)
        logo_scaled = pygame.transform.smoothscale(self.logo, (logo_width, logo_height))
        logo_x = self.resolution[0] // 2
        logo_y = int(self.resolution[1] * 0.05)
        logo_rect = logo_scaled.get_rect(midtop=(logo_x, logo_y))
        screen.blit(logo_scaled, logo_rect)

        # Tittle OSO
        font_title = pygame.font.SysFont("arial black", int(self.resolution[1] * 0.12))
        title_surface = font_title.render("OSO", True, (0, 0, 0))
        title_y = logo_rect.bottom + int(self.resolution[1] * 0.03)
        title_rect = title_surface.get_rect(center=(self.resolution[0] // 2, title_y))
        screen.blit(title_surface, title_rect)

        # Buttons
        for text, rect in self.buttons:
            self.draw_button(screen, text, rect)

    def draw_button(self, screen, text, rect):
        font_buttons = pygame.font.SysFont("arial black", int(rect.height * 0.5))
        
        # Hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            bg_color = (50, 50, 50)
        else:
            bg_color = (0, 0, 0) 

        pygame.draw.rect(screen, bg_color, rect, border_radius=int(rect.height * 0.15))
        label = font_buttons.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)