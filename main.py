import pygame
import sys
from screens.screen_manager import ScreenManager
from screens.screen_menu import ScreenMenu
import settings.settings_manager

pygame.init()

settings.settings_manager.ensure_max_resolution()

icon = pygame.image.load("assets/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("OSO-GAME")

# Load settings
resolution = settings.settings_manager.get_current_resolution()
opponent = settings.settings_manager.get_current_opponent()
board_size = settings.settings_manager.get_current_board_size()
language = settings.settings_manager.get_current_language()
screen =  ScreenManager.create_screen(resolution)
clock = pygame.time.Clock()

# Screen menu
manager = ScreenManager()
screen_menu = ScreenMenu(resolution, opponent, board_size, language, manager)
manager.set_screen(screen_menu)

# Game Loop
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Events
    manager.handle_events(events)
    manager.update()
    manager.draw(screen)

    pygame.display.flip()
    clock.tick(60)