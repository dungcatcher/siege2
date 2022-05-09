import pygame
from pygame import Vector2
import math
from astar_python.astar import Astar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        super().__init__()
        self.position = position  # Tile position
        self.pixel_position = [position[0] * tile_size + tile_size // 2, position[1] * tile_size + tile_size // 2]
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=self.pixel_position)
        self.path = []
        self.wall_obstructions = []
        self.path_searched = False
        self.vel = [0, 0]
        self.speed = 0.5
        self.target_index = 1
        self.health = 10
        self.worth = 10
        self.damage = 2
        self.range = 1.5
        self.original_cooldown = 30
        self.cooldown = self.original_cooldown
        self.closest_tower = None
        self.closest_tower_point = None

    def get_closest_tower(self, tower_group, search_walls=False):
        current_closest_point, current_closest_tower = None, None
        shortest_distance = 9999999
        for tower in tower_group:
            if (tower.is_wall and search_walls) or (not tower.is_wall and not search_walls):
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
        self.closest_tower_point = closest_point
        temp_obstructions = obstructions
        temp_obstructions[closest_point[1]][closest_point[0]] = 0  # Sets the target point to a crossable square
        astar = Astar(temp_obstructions)
        if self.position != closest_point:
            # path = astar.run(self.position, closest_point)
            # if path is not None:
            #     return path
            # else:  # Path could not be found, break walls to get through
            clear_map = [[0 for x in range(45)] for y in range(45)]  # No obstructions
            clear_astar = Astar(clear_map)
            clear_path = clear_astar.run(self.position, closest_point)
            for point in clear_path:
                for tower in tower_group:
                    if [tower.position[0], tower.position[1]] == point and tower.is_wall:
                        self.wall_obstructions.append(tower)
            return clear_path
        return []

    def attack(self, tower, game):
        tower.health -= self.damage
        if tower.health <= 0:
            game.sprite_groups["towers"].remove(tower)
            tower.kill()
            self.closest_tower = None
            self.path = []
            self.target_index = 1
            game.calculate_obstructions()
            self.path_searched = False
            if tower.is_town_hall:
                game.town_hall_destroyed = True

    def update(self, game):
        if not self.path_searched and game.sprite_groups["towers"]:
            self.path = self.pathfind_tower(game.sprite_groups["towers"], game.obstructions)
            self.path_searched = True

        if self.path:
            pixel_diff_vector = Vector2(self.path[self.target_index][0] * game.tile_size + game.tile_size / 2 - self.pixel_position[0],
                                 self.path[self.target_index][1] * game.tile_size + game.tile_size / 2 - self.pixel_position[1])
            pixel_distance_squared = pixel_diff_vector.length_squared()  # Ilmango efficient no square root
            if pixel_distance_squared != 0:
                pixel_diff_vector.normalize_ip()
            self.vel = pixel_diff_vector
            if pixel_distance_squared <= self.speed * self.speed:
                self.pixel_position = [self.path[self.target_index][0] * game.tile_size + game.tile_size / 2,
                                       self.path[self.target_index][1] * game.tile_size + game.tile_size / 2]
                if (self.target_index + 1) < len(self.path):
                    self.target_index += 1
        else:
            self.vel = [0, 0]

        #  Attack target tower when in range
        if self.closest_tower is not None:
            pixel_diff_vector = Vector2(self.closest_tower_point[0] * game.tile_size + game.tile_size // 2 - self.rect.centerx,
                                        self.closest_tower_point[1] * game.tile_size + game.tile_size // 2 - self.rect.centery)
            pixel_distance_squared = pixel_diff_vector.length_squared()
            if pixel_distance_squared <= (self.range * self.range) * (game.tile_size * game.tile_size):
                self.attack(self.closest_tower, game)
                self.vel = [0, 0]

        #  Attack wall obstructions when in range
        if self.wall_obstructions:
            closest_wall, closest_point = self.get_closest_tower(self.wall_obstructions, search_walls=True)
            pixel_diff_vector = Vector2(closest_wall.rect.centerx - self.rect.centerx,
                                        closest_wall.rect.centery - self.rect.centery)
            pixel_distance_squared = pixel_diff_vector.length_squared()
            if pixel_distance_squared <= (self.range * self.range) * (game.tile_size * game.tile_size):
                self.attack(closest_wall, game)
                if closest_wall.health <= 0:
                    self.wall_obstructions.remove(closest_wall)
                self.vel = [0, 0]

        self.position = [int(self.pixel_position[0] // game.tile_size), int(self.pixel_position[1] // game.tile_size)]
        self.pixel_position[0] += self.vel[0] * self.speed
        self.pixel_position[1] += self.vel[1] * self.speed
        self.rect.center = self.pixel_position
