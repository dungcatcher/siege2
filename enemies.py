import pygame
import pygame.math
import math
from astar_python.astar import Astar


class Enemy:
    def __init__(self, position, tile_size):
        self.position = position  # Tile position
        self.pixel_position = [position[0] * tile_size + tile_size // 2, position[1] * tile_size + tile_size // 2]
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=self.pixel_position)
        self.path = []
        self.vel = [0, 0]
        self.speed = 1
        self.target_index = 0

    def get_closest_tower(self, towers):
        current_closest_point, current_closest_tower = None, None
        shortest_distance = 999999
        for tower in towers:
            for point in tower.positions_covered:
                distance_to_point = math.hypot((self.position[0] - point[0]), (self.position[1] - point[1]))
                if distance_to_point < shortest_distance:
                    shortest_distance = distance_to_point
                    current_closest_point = point
                    current_closest_tower = tower

        return [current_closest_tower, current_closest_point]

    def pathfind_tower(self, towers):
        closest_tower, closest_point = self.get_closest_tower(towers)
        astar = Astar([[0 for x in range(36)] for y in range(36)])
        path = astar.run(self.position, closest_point)

        return path

    def update(self, tile_size, towers):
        if not self.path and towers:
            self.path = self.pathfind_tower(towers)

        if self.path:
            diff_vector = [self.path[self.target_index][0] - self.position[0],
                           self.path[self.target_index][1] - self.position[1]]
            pixel_diff_vector = [self.path[self.target_index][0] * tile_size + tile_size // 2 - self.pixel_position[0],
                                 self.path[self.target_index][1] * tile_size + tile_size // 2 - self.pixel_position[1]]
            pixel_distance = math.hypot(pixel_diff_vector[0], pixel_diff_vector[1])
            if pixel_distance <= self.speed:
                if (self.target_index + 1) < len(self.path):
                    self.target_index += 1
                else:
                    self.path = []
            self.vel = diff_vector
        else:
            self.vel = [0, 0]

        self.position = [self.pixel_position[0] // tile_size, self.pixel_position[1] // tile_size]
        self.pixel_position[0] += self.vel[0]
        self.pixel_position[1] += self.vel[1]
        self.rect.center = self.pixel_position

    def render(self, surface, tile_size):
        for point in self.path:
            rect = pygame.Rect(point[0] * tile_size, point[1] * tile_size, tile_size, tile_size)
            pygame.draw.rect(surface, (255, 200, 40), rect)
        surface.blit(self.image, self.rect)
