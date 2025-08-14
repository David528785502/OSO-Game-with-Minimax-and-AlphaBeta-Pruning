import pygame

pygame.init()

class ScreenManager:
    def __init__(self):
        self.current_screen = None

    def set_screen(self, screen):
        self.current_screen = screen

    def handle_events(self, events):
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self, surface):
        if self.current_screen:
            self.current_screen.draw(surface)

    def create_screen(resolution):
        return pygame.display.set_mode(resolution)

    def get_display_resolution():
        info = pygame.display.Info()
        return (info.current_w, info.current_h)