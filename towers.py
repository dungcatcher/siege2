import pygame
import math
from projectiles import Bullet, Bomb
from pygame import Vector2
from interpolate import colour_interpolate


class Tower(pygame.sprite.Sprite):
    def __init__(self, position, game):
        super().__init__()
        self.position = position  # Top left tile
        self.is_town_hall = False
        self.is_wall = False
        self.projectiles = []
        self.alive = True

    def draw_health_bar(self, surface):
        if self.health != self.max_health:
            health_rect = pygame.Rect(self.health_bar_rect.left, self.health_bar_rect.top,
                                      (self.health / self.max_health) * self.health_bar_rect.width, self.health_bar_rect.height)
            pygame.draw.rect(surface, colour_interpolate((0, 255, 0), (255, 0, 0), 1 - (self.health / self.max_health)), health_rect)
            pygame.draw.rect(surface, (0, 0, 0), self.health_bar_rect, width=1)

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
                if 0 <= new_position[0] < 45 and 0 <= new_position[1] < 45:
                    positions.append(new_position)

        return positions

    def update(self, game, sprite_groups):
        pass


class TownHall(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.is_town_hall = True
        self.size = (5, 5)  # Size in tiles
        self.image = pygame.image.load('Assets/townhall.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0] * game.tile_size, self.size[1] * game.tile_size))
        self.rect = self.image.get_rect(topleft=(self.position[0] * game.tile_size, self.position[1] * game.tile_size))
        self.positions_covered = self.calculate_positions_covered()
        self.max_health = 100
        self.health = self.max_health
        self.price = 0
        self.health_bar_rect = pygame.Rect(0, 0, self.rect.width * 0.85, self.rect.height * 0.25)
        self.health_bar_rect.midtop = (self.rect.centerx, self.rect.bottom + 10)


class GunTower(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.size = (3, 3)
        self.image = pygame.image.load('Assets/guntower.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0] * game.tile_size, self.size[1] * game.tile_size))
        self.rect = self.image.get_rect(topleft=(self.position[0] * game.tile_size, self.position[1] * game.tile_size))
        self.positions_covered = self.calculate_positions_covered()
        self.original_cooldown = 60
        self.cooldown = self.original_cooldown
        self.max_health = 30
        self.health = self.max_health
        self.price = 225
        self.range = 10
        self.health_bar_rect = pygame.Rect(0, 0, self.rect.width * 0.85, self.rect.height * 0.25)
        self.health_bar_rect.midtop = (self.rect.centerx, self.rect.bottom + 10)

    def update(self, game, sprite_groups):
        self.cooldown -= 1
        if self.cooldown <= 0:
            closest_enemy = self.get_closest_enemy(sprite_groups["enemies"])
            if closest_enemy:
                vector_to_enemy = Vector2(closest_enemy.rect.centerx - self.rect.centerx, closest_enemy.rect.centery - self.rect.centery)
                if vector_to_enemy.length_squared() < (self.range * self.range) * (game.tile_size * game.tile_size):
                    vector_to_enemy.normalize_ip()
                    sprite_groups["projectiles"].add(Bullet([self.rect.centerx, self.rect.centery], [vector_to_enemy[0], vector_to_enemy[1]]))
            self.cooldown = self.original_cooldown


class Wall(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.is_wall = True
        self.size = (1, 1)
        self.image_map = {
            "single": pygame.transform.scale(pygame.image.load('./Assets/single_wall.png'), (game.tile_size, game.tile_size)).convert_alpha(),
            "1_side": pygame.transform.scale(pygame.image.load('./Assets/wall_1_side.png'), (game.tile_size, game.tile_size)).convert_alpha(),
            "2_side": pygame.transform.scale(pygame.image.load('./Assets/wall_2_side.png'), (game.tile_size, game.tile_size)).convert_alpha(),
            "2_side_corner": pygame.transform.scale(pygame.image.load('./Assets/wall_2_side_corner.png'), (game.tile_size, game.tile_size)).convert_alpha(),
            "3_side": pygame.transform.scale(pygame.image.load('./Assets/wall_3_side.png'), (game.tile_size, game.tile_size)).convert_alpha(),
            "4_side": pygame.transform.scale(pygame.image.load('./Assets/wall_4_side.png'), (game.tile_size, game.tile_size)).convert_alpha()
        }
        self.image = self.image_map["single"]
        self.rect = self.image.get_rect(center=(self.position[0] * game.tile_size + game.tile_size / 2, self.position[1] * game.tile_size + game.tile_size / 2))
        self.positions_covered = self.calculate_positions_covered()
        self.max_health = 20
        self.health = self.max_health
        self.price = 10
        self.health_bar_rect = pygame.Rect(0, 0, self.rect.width * 0.85, self.rect.height * 0.25)
        self.health_bar_rect.midtop = (self.rect.centerx, self.rect.bottom + self.rect.height * 0.1)

    def update_image(self, game):  # Change image based on neighbouring walls
        neighbour_offsets = []

        side_offsets = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for offset in side_offsets:
            test_position = (self.position[0] + offset[0], self.position[1] + offset[1])
            if 1 <= test_position[0] <= 43 and 1 <= test_position[1] <= 43:
                for tower in game.sprite_groups["towers"]:
                    if tower.is_wall and tower.position == test_position and tower.position != self.position:
                        neighbour_offsets.append(offset)

        angle = 0
        if len(neighbour_offsets) == 1:
            angle = math.degrees(math.atan2(-neighbour_offsets[0][1], neighbour_offsets[0][0]))
            self.image = self.image_map["1_side"]
        elif len(neighbour_offsets) == 2:
            if (neighbour_offsets[0][0] == neighbour_offsets[1][0]) or (neighbour_offsets[0][1] == neighbour_offsets[1][1]):
                angle = math.degrees(math.atan2(-neighbour_offsets[0][1], neighbour_offsets[0][0]))
                self.image = self.image_map["2_side"]
            else:
                angles = []
                for offset in neighbour_offsets:
                    angles.append(math.degrees(math.atan2(-offset[1], offset[0])) % 360)

                if angles == [270, 0] or angles == [0, 270]:
                    angle = 270
                else:
                    avg_angle = sum(angles) / 2
                    angle = avg_angle - 45
                self.image = self.image_map["2_side_corner"]
        elif len(neighbour_offsets) == 3:
            self.image = self.image_map["3_side"]
            # ew
            if (-1, 0) in neighbour_offsets and (1, 0) in neighbour_offsets and (0, 1) in neighbour_offsets:
                angle = 180
            elif (0, 1) in neighbour_offsets and (0, -1) in neighbour_offsets:
                if (1, 0) in neighbour_offsets:
                    angle = 270
                elif (-1, 0) in neighbour_offsets:
                    angle = 90
        elif len(neighbour_offsets) == 4:
            self.image = self.image_map["4_side"]
        else:
            self.image = self.image_map["single"]

        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(self.position[0] * game.tile_size + game.tile_size / 2, self.position[1] * game.tile_size + game.tile_size / 2))


class Bomber(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.size = (3, 3)
        self.image = pygame.image.load('Assets/bomber.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size[0] * game.tile_size, self.size[1] * game.tile_size))
        self.rect = self.image.get_rect(topleft=(self.position[0] * game.tile_size, self.position[1] * game.tile_size))
        self.positions_covered = self.calculate_positions_covered()
        self.original_cooldown = 80
        self.cooldown = self.original_cooldown
        self.max_health = 50
        self.health = self.max_health
        self.price = 300
        self.range = 10
        self.health_bar_rect = pygame.Rect(0, 0, self.rect.width * 0.85, self.rect.height * 0.25)
        self.health_bar_rect.midtop = (self.rect.centerx, self.rect.bottom + 10)

    def update(self, game, sprite_groups):
        self.cooldown -= 1
        if self.cooldown <= 0:
            closest_enemy = self.get_closest_enemy(sprite_groups["enemies"])
            if closest_enemy:
                vector_to_enemy = Vector2(closest_enemy.rect.centerx - self.rect.centerx, closest_enemy.rect.centery - self.rect.centery)
                if vector_to_enemy.length_squared() < (self.range * self.range) * (game.tile_size * game.tile_size):
                    vector_to_enemy.normalize_ip()
                    sprite_groups["projectiles"].add(Bomb([self.rect.centerx, self.rect.centery], [vector_to_enemy[0], vector_to_enemy[1]]))
            self.cooldown = self.original_cooldown


name_to_class = {
    "Gun Tower": GunTower,
    "Wall": Wall,
    "Bomber": Bomber
}
