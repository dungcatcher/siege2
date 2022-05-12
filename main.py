import pygame
from towers import TownHall, name_to_class
from enemies import Enemy
from side_menu import SideMenu
import random
import json

pygame.init()

WINDOW = pygame.display.set_mode((900, 720))
ROWS, COLS = 45, 45


def generate_map(screen_size, tile_size):
    map_surface = pygame.Surface((screen_size[1], screen_size[1]), pygame.SRCALPHA)
    for x in range(map_surface.get_width() // tile_size):
        for y in range(map_surface.get_height() // tile_size):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            if (x + y) % 2 == 0:
                pygame.draw.rect(map_surface, (0, 255, 0), rect)
            else:
                pygame.draw.rect(map_surface, (30, 200, 30), rect)
            if x == 0 or x == COLS - 1 or y == 0 or y == ROWS - 1:
                pygame.draw.rect(map_surface, (60, 200, 60), rect)

    return map_surface


class EntityGroup(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            spr.draw_health_bar(surface)
        self.lostsprites = []


class Game:
    def __init__(self):
        self.money = 1000
        self.level = 0  # Not an index (subtract 1 to index)
        self.levels = [
          {"gap": 30, "amt": 20},
          {"gap": 20, "amt": 50},
          {"gap": 15, "amt": 70},
          {"gap": 10, "amt": 100},
          {"gap": 8, "amt": 150}
        ]
        self.original_levels = [
          {"gap": 30, "amt": 20},
          {"gap": 20, "amt": 50},
          {"gap": 15, "amt": 70},
          {"gap": 10, "amt": 100},
          {"gap": 8, "amt": 150}
        ]
        self.tile_size = WINDOW.get_height() // ROWS
        self.map_surface = generate_map(WINDOW.get_size(), self.tile_size)
        self.map_rect = self.map_surface.get_rect(topleft=(0, 0))
        self.side_menu = SideMenu(WINDOW.get_size(), self.map_surface.get_size())
        self.town_hall_placed = False
        self.town_hall_destroyed = False
        self.left_click = False
        self.mouse_position = [0, 0]
        self.bought_tower = None
        self.round_started = False  # Set to true for one frame
        self.round_over = True
        self.finished_spawning = True
        self.sprite_groups = {
            "towers": EntityGroup(),  # Extended group with health bars
            "enemies": EntityGroup(),
            "projectiles": pygame.sprite.Group()
        }
        self.obstructions = [[0 for x in range(COLS)] for y in range(ROWS)]
        self.enemy_spawnable_areas = self.calculate_enemy_spawnable_areas()

    def calculate_enemy_spawnable_areas(self):
        spawnable_areas = []
        for x in range(COLS):
            for y in range(ROWS):
                if not (1 <= x < COLS - 1 and 1 <= y < ROWS - 1):
                    spawnable_areas.append((x, y))

        return spawnable_areas

    def spawn_enemies(self):
        if self.level != 0:
            level_index = self.level - 1
            self.levels[level_index]["gap"] -= 1
            if self.levels[level_index]["gap"] <= 0:
                self.levels[level_index]["amt"] -= 1
                if self.levels[level_index]["amt"] > 0:
                    new_enemy = Enemy(random.choice(self.enemy_spawnable_areas), self)
                    self.sprite_groups["enemies"].add(new_enemy)
                    self.levels[level_index]["gap"] = self.original_levels[level_index]["gap"]
                else:
                    self.finished_spawning = True

    def calculate_obstructions(self):
        for tower in self.sprite_groups["towers"]:
            for position_covered in tower.positions_covered:
                self.obstructions[position_covered[1]][position_covered[0]] = None

    def check_placement_availability(self, tower):
        positions_covered = []  # Account for offscreen points this time
        for x in range(tower.size[0]):
            for y in range(tower.size[1]):
                positions_covered.append((tower.position[0] + x, tower.position[1] + y))

        for point in positions_covered:
            if not (1 <= point[0] < COLS - 1 and 1 <= point[1] < ROWS - 1):  # All points on the map
                return False
            elif self.obstructions[point[1]][point[0]] is None:
                return False
        return True

    def update(self):
        self.left_click = False
        self.mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.left_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.town_hall_placed:
                        self.round_started = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if len(self.sprite_groups["enemies"]) == 0 and self.finished_spawning:
            self.round_over = True

        if self.round_started and not self.town_hall_destroyed and self.round_over:
            if self.level + 1 <= len(self.levels):
                self.level += 1
                self.round_started = False
                self.finished_spawning = False
                self.round_over = False
            else:
                print('you win')

        if not self.finished_spawning:
            self.spawn_enemies()

        self.sprite_groups["towers"].update(self, self.sprite_groups)
        self.sprite_groups["enemies"].update(self)
        self.sprite_groups["projectiles"].update(self, self.sprite_groups)
        self.side_menu.update(self)

        if self.town_hall_destroyed:
            print('you lose')

        if self.round_over:
            if not self.town_hall_placed:
                if self.left_click and self.map_rect.collidepoint(self.mouse_position):
                    tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                    new_tower = TownHall(tile_position, self.tile_size)
                    if self.check_placement_availability(new_tower) and self.money - new_tower.price >= 0:
                        self.sprite_groups["towers"].add(new_tower)
                        self.town_hall_placed = True
                        self.calculate_obstructions()
                        self.money -= new_tower.price
            else:
                if self.left_click and self.map_rect.collidepoint(self.mouse_position) and self.bought_tower is not None:
                    tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                    new_tower = name_to_class[self.bought_tower.name](tile_position, self.tile_size)
                    if self.check_placement_availability(new_tower) and self.money - new_tower.price >= 0:
                        self.sprite_groups["towers"].add(new_tower)
                        self.calculate_obstructions()
                        self.money -= new_tower.price

    def render(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.map_surface, self.map_rect)
        self.sprite_groups["towers"].draw(surface)
        self.sprite_groups["enemies"].draw(surface)
        self.sprite_groups["projectiles"].draw(surface)
        self.side_menu.render(self, surface)


def main():
    clock = pygame.time.Clock()

    game = Game()

    while True:
        clock.tick(60)

        game.update()
        game.render(WINDOW)

        pygame.display.flip()


if __name__ == "__main__":
    main()
