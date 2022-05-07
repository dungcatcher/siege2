import pygame
from towers import TownHall, name_to_class
from enemies import Enemy
from side_menu import SideMenu
import random

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
        self.towers = []
        self.enemies = [Enemy((random.randint(0, COLS), random.randint(0, ROWS - 1)), self.tile_size)]
        self.map_surface = generate_map(WINDOW.get_size(), self.tile_size)
        self.map_rect = self.map_surface.get_rect(topleft=(0, 0))
        self.side_menu = SideMenu(WINDOW.get_size(), self.map_surface.get_size())
        self.town_hall_placed = False
        self.left_click = False
        self.mouse_position = [0, 0]
        self.bought_tower = None

    def update(self):
        self.left_click = False
        self.mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.left_click = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.side_menu.update(self)

        if not self.town_hall_placed:
            if self.left_click and self.map_rect.collidepoint(self.mouse_position):
                tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                new_tower = TownHall(tile_position, self.tile_size)
                self.towers.append(new_tower)
                self.town_hall_placed = True
        else:
            if self.left_click and self.map_rect.collidepoint(self.mouse_position):
                tile_position = (self.mouse_position[0] // self.tile_size, self.mouse_position[1] // self.tile_size)
                new_tower = name_to_class[self.bought_tower.name](tile_position, self.tile_size)
                self.towers.append(new_tower)

    def render(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.map_surface, self.map_rect)
        self.side_menu.render(surface)

        for tower in self.towers:
            tower.update(self.enemies)
            tower.render(surface)
        for enemy in self.enemies:
            enemy.update(self.tile_size, self.towers)
            enemy.render(surface, self.tile_size)


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
