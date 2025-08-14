import pygame
import sys
import os
import json
from game.game_manager import GameManager
from ai.ai_manager import AIManager

class ScreenGame:
    def __init__(self, resolution, opponent, board_size, language, manager):
        pygame.font.init()
        self.resolution = resolution
        self.opponent = opponent
        self.board_size = board_size
        self.language = language
        self.manager = manager
        
        base_dir = os.path.dirname(os.path.dirname(__file__))
        lang_path = os.path.join(base_dir, "languages", "languages.json")
        with open(lang_path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

        self.game_manager = GameManager(board_size)
        self.ai_manager = AIManager(self.game_manager, ai_player=2)

        self.game_manager.set_selected_letter('S')

        self.screen_width, self.screen_height = resolution

        self.grid_side_w = int(self.screen_width * 0.6)
        self.info_side_w = int(self.screen_width * 0.34)
        self.margin_lr = int(self.screen_width * 0.03)

        self.grid_top_margin = int(self.screen_height * 0.10)
        self.grid_bottom_margin = int(self.screen_height * 0.10)
        self.grid_height = int(self.screen_height * 0.80)
        self.cell_size = self.grid_height // self.board_size
        self.grid_width = self.cell_size * self.board_size
        self.grid_x = self.margin_lr
        self.grid_y = self.grid_top_margin

        self.info_x = self.grid_x + self.grid_width + self.margin_lr
        self.info_y = 0

        self.color_bg = (255, 255, 255)
        self.color_panel_bg = (255, 255, 255)
        self.color_grid_lines = (50, 50, 50)
        self.color_red = (200, 30, 30)
        self.color_blue = (30, 30, 200)
        self.color_black = (0, 0, 0)

        self.font_turn = pygame.font.SysFont(None, max(28, self.screen_width // 20))
        self.font_points = pygame.font.SysFont(None, max(22, self.screen_width // 20))
        self.font_button = pygame.font.SysFont(None, max(40, self.screen_width // 8))
        self.font_back_button = pygame.font.SysFont(None, max(20, self.screen_width // 16))

        self.buttons = {}
        self.create_ui_elements()

        self.arrow_size = max(16, self.cell_size // 3)
        self.game_over = False

        self.letters_color = {}
        
    def create_ui_elements(self):
        container_w = int(self.screen_width * 0.34)
        margin_x = int(self.screen_width * 0.05)
        y_start = int(self.screen_height * 0.08)

        self.turn_rect = pygame.Rect(self.info_x + margin_x, y_start, container_w - 2 * margin_x, int(self.screen_height * 0.05))
        self.current_player_rect = pygame.Rect(self.info_x + margin_x, y_start + int(self.screen_height * 0.07), container_w - 2 * margin_x, int(self.screen_height * 0.04))
        self.points_label_rect = pygame.Rect(self.info_x + margin_x, y_start + int(self.screen_height * 0.12), container_w - 2 * margin_x, int(self.screen_height * 0.05))
        self.p1_points_rect = pygame.Rect(self.info_x + margin_x, y_start + int(self.screen_height * 0.18), container_w - 2 * margin_x, int(self.screen_height * 0.04))
        self.p2_points_rect = pygame.Rect(self.info_x + margin_x, y_start + int(self.screen_height * 0.24), container_w - 2 * margin_x, int(self.screen_height * 0.04))
        self.select_letter_label_rect = pygame.Rect(self.info_x + margin_x, y_start + int(self.screen_height * 0.30), container_w - 2 * margin_x, int(self.screen_height * 0.05))

        button_w = max(60, int(self.screen_width * 0.12))
        button_h = button_w 
        buttons_y = y_start + int(self.screen_height * 0.55)

        btn_spacing = int(self.screen_width * 0.015)
        total_btn_width = button_w * 2 + btn_spacing
        start_x = self.info_x + (container_w - total_btn_width) // 2

        self.buttons['O'] = pygame.Rect(start_x, buttons_y, button_w, button_h)
        self.buttons['S'] = pygame.Rect(start_x + button_w + btn_spacing, buttons_y, button_w, button_h)

        back_w = int(self.screen_width * 0.25)
        back_h = int(self.screen_height * 0.07)
        back_x = self.info_x + container_w - back_w - int(self.screen_width * 0.02)
        back_y = self.screen_height - back_h - int(self.screen_height * 0.02)

        self.buttons['back'] = pygame.Rect(back_x, back_y, back_w, back_h)

    def handle_events(self, events):
        if self.game_over:
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.buttons['back'].collidepoint(event.pos):
                        from screens.screen_menu import ScreenMenu
                        self.manager.set_screen(ScreenMenu(
                            self.resolution,
                            self.opponent,
                            self.board_size,
                            self.language,
                            self.manager
                        ))
            return

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if self.grid_x <= mx < self.grid_x + self.grid_width and self.grid_y <= my < self.grid_y + self.grid_height:
                    if self.opponent == 'human':
                        current_player = self.game_manager.get_current_player()
                        valid, points = self.game_manager.place_letter(
                            (my - self.grid_y) // self.cell_size,
                            (mx - self.grid_x) // self.cell_size)
                        if valid:
                            self.letters_color[((my - self.grid_y) // self.cell_size,
                                                (mx - self.grid_x) // self.cell_size)] = self.color_red if current_player == 1 else self.color_blue
                            
                            if self.game_manager.is_full():
                                self.game_over = True

                    elif self.opponent in ('ai', 'ia'):
                        current_player = self.game_manager.get_current_player()
                        if current_player == 1:
                            valid, points = self.game_manager.place_letter(
                                (my - self.grid_y) // self.cell_size,
                                (mx - self.grid_x) // self.cell_size)
                            if valid:
                                placed_player = 1
                                self.letters_color[((my - self.grid_y) // self.cell_size,
                                                    (mx - self.grid_x) // self.cell_size)] = self.color_red
                                if self.game_manager.is_full():
                                    self.game_over = True
                                else:
                                    while self.game_manager.get_current_player() == 2:
                                        ai_move = self.ai_manager.best_move()
                                        if not ai_move:
                                            break

                                        r, c, letter = ai_move
                                        self.game_manager.set_selected_letter(letter)
                                        valid_ai, points_ai = self.game_manager.place_letter(r, c)

                                        if valid_ai:
                                            self.letters_color[(r, c)] = self.color_blue

                                        if self.game_manager.is_full():
                                            self.game_over = True
                                            break

                for letter in ('O', 'S'):
                    if self.buttons[letter].collidepoint(mx, my):
                        if self.opponent == 'human' or (self.opponent in ('ai', 'ia') and self.game_manager.get_current_player() == 1):

                            self.game_manager.set_selected_letter(letter)

                if self.buttons['back'].collidepoint(mx, my):
                    from screens.screen_menu import ScreenMenu
                    self.manager.set_screen(ScreenMenu(
                        self.resolution,
                        self.opponent,
                        self.board_size,
                        self.language,
                        self.manager
                    ))

    def draw(self, surface):
        surface.fill(self.color_bg)

        grid_rect = pygame.Rect(self.grid_x, self.grid_y, self.grid_width, self.grid_height)
        pygame.draw.rect(surface, self.color_bg, grid_rect)
        pygame.draw.rect(surface, self.color_black, grid_rect, 2)

        for i in range(1, self.board_size):
            x = self.grid_x + i * self.cell_size
            pygame.draw.line(surface, self.color_grid_lines, (x, self.grid_y), (x, self.grid_y + self.grid_height), 2)
        for i in range(1, self.board_size):
            y = self.grid_y + i * self.cell_size
            pygame.draw.line(surface, self.color_grid_lines, (self.grid_x, y), (self.grid_x + self.grid_width, y), 2)

        for r in range(self.board_size):
            for c in range(self.board_size):
                letter = self.game_manager.board[r][c]
                if letter != '':
                    center_x = self.grid_x + c * self.cell_size + self.cell_size // 2
                    center_y = self.grid_y + r * self.cell_size + self.cell_size // 2
                    color = self.letters_color.get((r, c), self.color_black)
                    letter_render = self.font_turn.render(letter, True, color)
                    letter_rect = letter_render.get_rect(center=(center_x, center_y))
                    surface.blit(letter_render, letter_rect)

        info_rect = pygame.Rect(self.info_x, 0, self.info_side_w, self.screen_height)
        pygame.draw.rect(surface, self.color_panel_bg, info_rect)

        margin_x = int(self.info_side_w * 0.05)
        y = int(self.screen_height * 0.05)
        spacing_block = int(self.screen_height * 0.08)
        spacing_line = int(self.screen_height * 0.015)

        center_x = self.info_x + self.info_side_w // 2

        # 1. Turn
        turn_text = self.translations[self.language]['turn']
        turn_render = self.font_turn.render(turn_text, True, self.color_black)
        turn_rect = turn_render.get_rect(center=(center_x, y + turn_render.get_height() // 2))
        surface.blit(turn_render, turn_rect)

        y += turn_render.get_height() + spacing_line

        # 2. Players
        current_player = self.game_manager.get_current_player()
        player_key = 'player_1' if current_player == 1 else 'player_2'
        player_text = self.translations[self.language][player_key]
        player_color = self.color_red if current_player == 1 else self.color_blue
        player_render = self.font_points.render(player_text, True, player_color)
        player_rect = player_render.get_rect(center=(center_x, y + player_render.get_height() // 2))
        surface.blit(player_render, player_rect)

        y += player_render.get_height() + spacing_block

        # 3. Points label
        points_text = self.translations[self.language]['points']
        points_render = self.font_turn.render(points_text, True, self.color_black)
        points_rect = points_render.get_rect(center=(center_x, y + points_render.get_height() // 2))
        surface.blit(points_render, points_rect)

        y += points_render.get_height() + spacing_line

        # 4. Player 1 points
        p1_points = self.game_manager.get_player_points(1)
        p1_text = f"{self.translations[self.language]['player_1']}: {p1_points:02d}"
        p1_render = self.font_points.render(p1_text, True, self.color_red)
        p1_rect = p1_render.get_rect(topleft=(self.info_x + margin_x, y))
        surface.blit(p1_render, p1_rect)

        y += p1_render.get_height() + spacing_line

        # 5. Player 2 points
        p2_points = self.game_manager.get_player_points(2)
        p2_text = f"{self.translations[self.language]['player_2']}: {p2_points:02d}"
        p2_render = self.font_points.render(p2_text, True, self.color_blue)
        p2_rect = p2_render.get_rect(topleft=(self.info_x + margin_x, y))
        surface.blit(p2_render, p2_rect)

        y += p2_render.get_height() + spacing_block

        # 6. Select letter
        sel_letter_text = self.translations[self.language]['select_letter']
        sel_letter_render = self.font_points.render(sel_letter_text, True, self.color_black)
        sel_letter_rect = sel_letter_render.get_rect(center=(center_x, y + sel_letter_render.get_height() // 2))
        surface.blit(sel_letter_render, sel_letter_rect)

        y += sel_letter_render.get_height() + int(self.screen_height * 0.015)

        # Buttons O and S
        total_btn_width = sum(btn.width for btn in [self.buttons['O'], self.buttons['S']]) + int(self.screen_width * 0.015)
        btn_start_x = center_x - total_btn_width // 2

        for i, letter in enumerate(('O', 'S')):
            btn_rect = self.buttons[letter]
            btn_rect.x = btn_start_x
            btn_rect.y = y
            btn_start_x += btn_rect.width + int(self.screen_width * 0.015)

            current_turn_color = self.color_red if self.game_manager.get_current_player() == 1 else self.color_blue
            pygame.draw.rect(surface, current_turn_color, btn_rect, border_radius=8)
            if self.game_manager.get_selected_letter() == letter:
                pygame.draw.rect(surface, self.color_black, btn_rect, 3, border_radius=8)
            else:
                pygame.draw.rect(surface, self.color_black, btn_rect, 1, border_radius=8)

            letter_render = self.font_button.render(letter, True, self.color_bg)
            letter_rect = letter_render.get_rect(center=btn_rect.center)
            surface.blit(letter_render, letter_rect)

        # Arrow
        selected_letter = self.game_manager.get_selected_letter()
        selected_btn = self.buttons[selected_letter]
        tri_x = selected_btn.centerx
        tri_y = selected_btn.bottom + int(self.screen_height * 0.01)
        tri_size = max(16, self.cell_size // 3)
        self.draw_triangle(surface, tri_x, tri_y, tri_size, self.color_black)

        # Back Button
        mouse_pos = pygame.mouse.get_pos()
        back_rect = self.buttons['back']
        is_hovered = back_rect.collidepoint(mouse_pos)

        if not hasattr(self, "back_hover_color"):
            self.back_hover_color = [0, 0, 0]

        target_color = [50, 50, 50] if is_hovered else [0, 0, 0]

        for i in range(3):
            self.back_hover_color[i] += (target_color[i] - self.back_hover_color[i]) * 0.15

        pygame.draw.rect(surface, self.back_hover_color, back_rect, border_radius=12)
        pygame.draw.rect(surface, self.color_black, back_rect, width=2, border_radius=12)

        back_text = self.translations[self.language]['back']
        back_render = self.font_back_button.render(back_text, True, (255, 255, 255))
        back_rect_text = back_render.get_rect(center=back_rect.center)
        surface.blit(back_render, back_rect_text)

        if self.game_over:
            winner = self.game_manager.get_winner()
            if winner == 0:
                winner_text = self.translations[self.language]['draw']
            else:
                winner_text = f"{self.translations[self.language]['winner']}: {self.translations[self.language][f'player_{winner}']}"
            font_winner = pygame.font.SysFont(None, max(36, self.screen_width // 25))
            winner_render = font_winner.render(winner_text, True, self.color_black)
            winner_rect = winner_render.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            surface.blit(winner_render, winner_rect)

    def draw_triangle(self, surface, x, y, size, color):
        points = [(x, y), (x - size // 2, y + size), (x + size // 2, y + size)]
        pygame.draw.polygon(surface, color, points)

    def update(self):
        pass