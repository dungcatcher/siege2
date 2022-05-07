import pygame
import math
from projectiles import Projectile
from pygame import Vector2


class Tower(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        super().__init__()
        self.position = position  # Top left tile
        self.is_town_hall = False
        self.projectiles = []

    def get_closest_enemy(self, enemy_group):
        current_closest_point, current_closest_enemy = None, None
        shortest_distance = 9999999
        for enemy in enemy_group:
            distance_to_point = math.hypot((self.rect.centerx - enemy.pixel_position[0]), (self.rect.centery - enemy.pixel_position[1]))
            if distance_to_point < shortest_distance:
                shortest_distance = distance_to_point
                current_closest_point = enemy.pixel_position
                current_closest_enemy = enemy

        return current_closest_enemy

    def calculate_positions_covered(self):
        positions = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                new_position = (self.position[0] + x, self.position[1] + y)
                positions.append(new_position)

        return positions

    def update(self, sprite_groups):
        pass


class TownHall(Tower):
    def __init__(self, position, tile_size):
        super().__init__(position, tile_size)
        self.is_town_hall = True
        self.size = (5, 5)  # Size in tiles
        self.image = pygame.image.load('Assets/townhall.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0] * tile_size, self.size[1] * tile_size))
        self.rect = self.image.get_rect(topleft=(self.position[0] * tile_size, self.position[1] * tile_size))
        self.positions_covered = self.calculate_positions_covered()


class GunTower(Tower):
    def __init__(self, position, tile_size):
        super().__init__(position, tile_size)
        self.size = (3, 3)
        self.image = pygame.image.load('Assets/guntower.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0] * tile_size, self.size[1] * tile_size))
        self.rect = self.image.get_rect(topleft=(self.position[0] * tile_size, self.position[1] * tile_size))
        self.positions_covered = self.calculate_positions_covered()

    def update(self, sprite_groups):
        closest_enemy = self.get_closest_enemy(sprite_groups["enemies"])
        vector_to_enemy = Vector2(closest_enemy.rect.centerx - self.rect.centerx, closest_enemy.rect.centery - self.rect.centery)
        vector_to_enemy.normalize_ip()
        sprite_groups["projectiles"].add(Projectile([self.rect.centerx, self.rect.centery], [vector_to_enemy[0], vector_to_enemy[1]]))

        for projectile in self.projectiles:
            projectile.update()


name_to_class = {
    "Gun Tower": GunTower
}
