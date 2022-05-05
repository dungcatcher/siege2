import pygame
from towers import TownHall
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


def main():
    clock = pygame.time.Clock()

    tile_size = WINDOW.get_height() // ROWS
    towers = []
    enemies = [Enemy((random.randint(0, COLS), random.randint(0, ROWS - 1)), tile_size)]

    map_surface = generate_map(WINDOW.get_size(), tile_size)
    map_rect = map_surface.get_rect(topleft=(0, 0))

    money = 500
    side_menu = SideMenu(WINDOW.get_size(), map_surface.get_size(), money)

    left_click = False
    town_hall_placed = False

    while True:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        WINDOW.blit(map_surface, map_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        side_menu.render(WINDOW)
        side_menu.update(left_click, (mouse_x, mouse_y))

        if not town_hall_placed:
            if left_click:
                if map_rect.collidepoint((mouse_x, mouse_y)):
                    tile_position = (mouse_x // tile_size, mouse_y // tile_size)
                    new_tower = TownHall(tile_position, tile_size)
                    towers.append(new_tower)
                    town_hall_placed = True

        for tower in towers:
            tower.render(WINDOW)
        for enemy in enemies:
            enemy.update(tile_size, towers)
            enemy.render(WINDOW, tile_size)

        left_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_click = True

        pygame.display.flip()


main()
