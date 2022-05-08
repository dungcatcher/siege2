import pygame
from pygame import Vector2
import math
from astar_python.astar import Astar
import time


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        super().__init__()
        self.position = position  # Tile position
        self.pixel_position = [position[0] * tile_size + tile_size // 2, position[1] * tile_size + tile_size // 2]
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=self.pixel_position)
        self.path = []
        self.path_searched = False
        self.vel = [0, 0]
        self.speed = 0.5
        self.target_index = 1
        self.health = 10
        self.worth = 10
        self.damage = 2
        self.range = 5
        self.original_cooldown = 30
        self.cooldown = self.original_cooldown
        self.closest_tower = None

    def get_closest_tower(self, tower_group, search_walls=False):
        current_closest_point, current_closest_tower = None, None
        shortest_distance = 9999999
        for tower in tower_group:
            if not tower.is_wall and not search_walls:
                for point in tower.positions_covered:
                    distance_to_point = math.hypot((self.position[0] - point[0]), (self.position[1] - point[1]))
                    if distance_to_point < shortest_distance:
                        shortest_distance = distance_to_point
                        current_closest_point = point
                        current_closest_tower = tower

        return [current_closest_tower, current_closest_point]

    def pathfind_tower(self, tower_group, obstructions):
        closest_tower, closest_point = self.get_closest_tower(tower_group)
        self.closest_tower = closest_tower
        temp_obstructions = obstructions
        temp_obstructions[closest_point[1]][closest_point[0]] = 0  # Sets the target point to a crossable square
        astar = Astar(temp_obstructions)
        if self.position != closest_point:
            path = astar.run(self.position, closest_point)
            if path is not None:
                return path
        return []

    def attack(self, tower, game):
        tower.health -= self.damage
        if tower.health <= 0:
            game.sprite_groups["towers"].remove(tower)
            game.calculate_obstructions()

    def update(self, game):
        if not self.path_searched and game.sprite_groups["towers"]:
            self.path = self.pathfind_tower(game.sprite_groups["towers"], game.obstructions)
            self.path_searched = True

        if self.path:
            pixel_diff_vector = Vector2(self.path[self.target_index][0] * game.tile_size + game.tile_size / 2 - self.pixel_position[0],
                                 self.path[self.target_index][1] * game.tile_size + game.tile_size / 2 - self.pixel_position[1])
            pixel_distance_squared = pixel_diff_vector.length_squared()  # Ilmango efficient no square root
            pixel_diff_vector.normalize_ip()
            self.vel = pixel_diff_vector
            if pixel_distance_squared <= self.speed * self.speed:
                self.pixel_position = [self.path[self.target_index][0] * game.tile_size + game.tile_size / 2,
                                       self.path[self.target_index][1] * game.tile_size + game.tile_size / 2]
                if (self.target_index + 1) < len(self.path):
                    self.target_index += 1
        else:
            self.vel = [0, 0]

        if self.closest_tower is not None:
            pixel_diff_vector = Vector2(self.closest_tower.rect.centerx - self.rect.centerx,
                                        self.closest_tower.rect.centery - self.rect.centery)
            pixel_distance_squared = pixel_diff_vector.length_squared()
            print(pixel_distance_squared <= (self.range * self.range) * game.tile_size)
            if pixel_distance_squared <= (self.range * self.range) * (game.tile_size * game.tile_size):
                self.attack(self.closest_tower, game)

        self.position = [int(self.pixel_position[0] // game.tile_size), int(self.pixel_position[1] // game.tile_size)]
        self.pixel_position[0] += self.vel[0] * self.speed
        self.pixel_position[1] += self.vel[1] * self.speed
        self.rect.center = self.pixel_position
