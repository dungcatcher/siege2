import pygame
from towers import TownHall, name_to_class
from enemies import Enemy
from side_menu import SideMenu
import random
import time

pygame.init()

WINDOW = pygame.display.set_mode((900, 720))
ROWS, COLS = 45, 45


def generate_map(screen_size, tile_size):
    map_surface = pygame.Surface((screen_size[1], screen_size[1]))
    for x in range(map_surface.get_width() // tile_size):
        for y in range(map_surface.get_height() // tile_size):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            if (x + y) % 2 == 0:
                pygame.draw.rect(map_surface, (0, 255, 0), rect)
            else:
                pygame.draw.rect(map_surface, (30, 200, 30), rect)

    return map_surface


class Game:
    def __init__(self):
        self.money = 500
        self.tile_size = WINDOW.get_height() // ROWS
        self.map_surface = generate_map(WINDOW.get_size(), self.tile_size)
        self.map_rect = self.map_surface.get_rect(topleft=(0, 0))
        self.side_menu = SideMenu(WINDOW.get_size(), self.map_surface.get_size())
        self.town_hall_placed = False
        self.left_click = False
        self.mouse_position = [0, 0]
        self.bought_tower = None
        self.sprite_groups = {
            "towers": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(Enemy((random.randint(0, COLS), random.randint(0, ROWS - 1)), self.tile_size)),
            "projectiles": pygame.sprite.Group()
        }
        self.obstructions = [[0 for x in range(COLS)] for y in range(ROWS)]

    def calculate_obstructions(self):
        for tower in self.sprite_groups["towers"]:
            for position_covered in tower.positions_covered:
                self.obstructions[position_covered[1]][position_covered[0]] = None

    def update(self):
        self.left_click = False
        self.mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.left_click = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.sprite_groups["towers"].update(self.sprite_groups)
        self.sprite_groups["enemies"].update(self.tile_size, self.sprite_groups, self.obstructions)
        self.sprite_groups["projectiles"].update()
        self.side_menu.update(self)

        if not self.town_hall_placed:
            if self.left_click and self.map_rect.collidepoint(self.mouse_position):
                tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                new_tower = TownHall(tile_position, self.tile_size)
                self.sprite_groups["towers"].add(new_tower)
                self.town_hall_placed = True
                self.calculate_obstructions()
        else:
            if self.left_click and self.map_rect.collidepoint(self.mouse_position) and self.bought_tower is not None:
                tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                new_tower = name_to_class[self.bought_tower.name](tile_position, self.tile_size)
                self.sprite_groups["towers"].add(new_tower)
                self.calculate_obstructions()

    def render(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.map_surface, self.map_rect)
        self.sprite_groups["towers"].draw(surface)
        self.sprite_groups["enemies"].draw(surface)
        self.sprite_groups["projectiles"].draw(surface)
        self.side_menu.render(surface)


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
