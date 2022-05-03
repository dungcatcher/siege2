import pygame


class Tower:
    def __init__(self, position, tile_size):
        self.position = position  # Top left tile


class TownHall(Tower):
    def __init__(self, position, tile_size):
        super().__init__(position, tile_size)
        self.size = (5, 5)  # Size in tiles
        self.image = pygame.Surface((self.size[0] * tile_size, self.size[1] * tile_size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.position[0] * tile_size, self.position[1] * tile_size))

    def render(self, surface):
        surface.blit(self.image, self.rect)
