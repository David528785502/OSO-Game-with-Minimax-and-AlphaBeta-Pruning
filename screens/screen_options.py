import pygame
import json
import os
import settings.settings_manager as settings_manager

class ScreenOptions:
    def __init__(self, resolution, opponent, board_size, language, manager):
        self.resolution = resolution
        self.opponent = opponent
        self.board_size = board_size
        self.language = language
        self.manager = manager

        # Load translations
        base_dir = os.path.dirname(os.path.dirname(__file__))
        lang_path = os.path.join(base_dir, "languages", "languages.json")
        with open(lang_path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

        # Load settings
        self.settings = settings_manager.load_settings()

        # Options lists
        self.resolutions = settings_manager.get_resolutions()
        self.opponents = settings_manager.get_opponents()
        self.board_sizes = settings_manager.get_board_sizes()
        self.languages = settings_manager.get_languages()

        # Current indices
        self.current_res_index = self.resolutions.index(resolution)
        self.current_opp_index = self.opponents.index(opponent)
        self.current_board_index = self.board_sizes.index(board_size)
        self.current_lang_index = self.languages.index(language)

        # Font
        self.font = pygame.font.SysFont("arial", int(resolution[1] * 0.05))

        # Layout
        self.update_layout()

        # Colors and hover
        self.hover_fill = (200, 200, 200)
        self.normal_fill = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.triangle_fill = (255, 255, 255)
        self.triangle_border = (0, 0, 0)
        self.text_color = (0, 0, 0)

        self.rects = {}
        self.back_rect = None

    def draw_rounded_rect(self, surface, rect, color, border_color, border_radius=10, border_width=2):
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)
        pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=border_radius)

    def draw_triangle(self, surface, points, fill_color, border_color):
        pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, border_color, points, 2)

    def draw_option(self, surface, label, value, y, key):
        mouse_pos = pygame.mouse.get_pos()

        # Label
        label_text = f"{label}: "
        label_surf = self.font.render(label_text, True, self.text_color)
        label_rect = label_surf.get_rect(topleft=(self.label_x, y))
        surface.blit(label_surf, label_rect)

        # Value
        value_surf = self.font.render(value, True, self.text_color)
        arrow_size = max(int(self.resolution[1] * 0.06), 30)
        center_y = y + arrow_size // 2

        value_rect = value_surf.get_rect()
        value_rect.topleft = (self.value_x, center_y - value_rect.height // 2)
        value_bg_rect = value_rect.inflate(40, 20)

        # Rectangle
        self.draw_rounded_rect(surface, value_bg_rect, self.normal_fill, self.border_color, border_radius=12, border_width=2)
        surface.blit(value_surf, value_rect)

        # Arrows
        left_arrow_rect = pygame.Rect(
            value_bg_rect.left - self.arrow_spacing - arrow_size,
            center_y - arrow_size // 2,
            arrow_size,
            arrow_size
        )
        right_arrow_rect = pygame.Rect(
            value_bg_rect.right + self.arrow_spacing,
            center_y - arrow_size // 2,
            arrow_size,
            arrow_size
        )

        left_points = [
            (left_arrow_rect.right, left_arrow_rect.top),
            (left_arrow_rect.left, left_arrow_rect.centery),
            (left_arrow_rect.right, left_arrow_rect.bottom),
        ]
        right_points = [
            (right_arrow_rect.left, right_arrow_rect.top),
            (right_arrow_rect.right, right_arrow_rect.centery),
            (right_arrow_rect.left, right_arrow_rect.bottom),
        ]

        left_fill = self.hover_fill if left_arrow_rect.collidepoint(mouse_pos) else self.triangle_fill
        right_fill = self.hover_fill if right_arrow_rect.collidepoint(mouse_pos) else self.triangle_fill

        self.draw_triangle(surface, left_points, left_fill, self.triangle_border)
        self.draw_triangle(surface, right_points, right_fill, self.triangle_border)

        self.rects[f"{key}_left"] = left_arrow_rect
        self.rects[f"{key}_right"] = right_arrow_rect

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Resolution
                if self.rects['res_left'].collidepoint(mx, my):
                    self.current_res_index = (self.current_res_index - 1) % len(self.resolutions)
                elif self.rects['res_right'].collidepoint(mx, my):
                    self.current_res_index = (self.current_res_index + 1) % len(self.resolutions)
                if self.rects['res_left'].collidepoint(mx, my) or self.rects['res_right'].collidepoint(mx, my):
                    new_res = self.resolutions[self.current_res_index]
                    self.settings["current_resolution"] = new_res
                    settings_manager.save_settings(self.settings)
                    pygame.display.set_mode(new_res)
                    self.resolution = new_res
                    self.update_layout()

                # Opponent
                elif self.rects['opp_left'].collidepoint(mx, my):
                    self.current_opp_index = (self.current_opp_index - 1) % len(self.opponents)
                elif self.rects['opp_right'].collidepoint(mx, my):
                    self.current_opp_index = (self.current_opp_index + 1) % len(self.opponents)
                if self.rects['opp_left'].collidepoint(mx, my) or self.rects['opp_right'].collidepoint(mx, my):
                    self.settings["current_opponent"] = self.opponents[self.current_opp_index]
                    settings_manager.save_settings(self.settings)
                    self.opponent = self.opponents[self.current_opp_index]

                # Board size
                elif self.rects['board_left'].collidepoint(mx, my):
                    self.current_board_index = (self.current_board_index - 1) % len(self.board_sizes)
                elif self.rects['board_right'].collidepoint(mx, my):
                    self.current_board_index = (self.current_board_index + 1) % len(self.board_sizes)
                if self.rects['board_left'].collidepoint(mx, my) or self.rects['board_right'].collidepoint(mx, my):
                    self.settings["current_board_size"] = self.board_sizes[self.current_board_index]
                    settings_manager.save_settings(self.settings)
                    self.board_size = self.board_sizes[self.current_board_index]

                # Language
                elif self.rects['lang_left'].collidepoint(mx, my):
                    self.current_lang_index = (self.current_lang_index - 1) % len(self.languages)
                elif self.rects['lang_right'].collidepoint(mx, my):
                    self.current_lang_index = (self.current_lang_index + 1) % len(self.languages)
                if self.rects['lang_left'].collidepoint(mx, my) or self.rects['lang_right'].collidepoint(mx, my):
                    new_lang = self.languages[self.current_lang_index]
                    self.settings["current_language"] = new_lang
                    settings_manager.save_settings(self.settings)
                    self.language = new_lang

                # Back
                elif self.back_rect and self.back_rect.collidepoint(mx, my):
                    from screens.screen_menu import ScreenMenu
                    self.manager.set_screen(ScreenMenu(
                        self.resolution,
                        self.opponent,
                        self.board_size,
                        self.language,
                        self.manager
                    ))

    def draw(self, surface):
        surface.fill((255, 255, 255))
        tr = self.translations.get(self.language, self.translations["en"])
        y = self.start_y

        self.draw_option(surface, tr.get("resolution", "Resolution"), f"{self.resolutions[self.current_res_index][0]}x{self.resolutions[self.current_res_index][1]}", y, "res")
        y += self.spacing

        current_opp_key = self.opponents[self.current_opp_index]
        opp_index = self.opponents.index(current_opp_key)
        current_opp_text = tr["opponents"][opp_index]
        self.draw_option(surface, tr.get("opponent", "Opponent"), current_opp_text, y, "opp")
        y += self.spacing

        self.draw_option(surface, tr.get("board", "Board"), f"{self.board_sizes[self.current_board_index]}x{self.board_sizes[self.current_board_index]}", y, "board")
        y += self.spacing
        self.draw_option(surface, tr.get("language", "Language"), self.languages[self.current_lang_index].upper(), y, "lang")

        # Back button
        y += int(self.spacing * 1.5)
        mouse_pos = pygame.mouse.get_pos()
        back_text = tr.get("back", "Back")
        back_surf = self.font.render(back_text, True, self.text_color)
        text_rect = back_surf.get_rect(center=(self.resolution[0] // 2, y))
        self.back_rect = text_rect.inflate(30, 15)

        if self.back_rect.collidepoint(mouse_pos):
            self.draw_rounded_rect(surface, self.back_rect, self.hover_fill, self.border_color, border_radius=12, border_width=2)
        else:
            self.draw_rounded_rect(surface, self.back_rect, self.normal_fill, self.border_color, border_radius=12, border_width=2)

        surface.blit(back_surf, text_rect)

    def update_layout(self):
        self.font = pygame.font.SysFont("arial", int(self.resolution[1] * 0.05))
        self.label_x = int(self.resolution[0] * 0.25)
        self.value_x = int(self.resolution[0] * 0.54)
        self.arrow_spacing = int(self.resolution[0] * 0.01)
        self.start_y = int(self.resolution[1] * 0.20)
        self.spacing = int(self.resolution[1] * 0.15)

    def update(self):
        pass