import pygame


class SideMenu:
    def __init__(self, screen_size, map_size):
        self.rect = pygame.Rect(map_size[0], 0, (screen_size[0] - map_size[0]), screen_size[1])

    def render(self, surface):
        pygame.draw.rect(surface, (30, 30, 70), self.rect)
