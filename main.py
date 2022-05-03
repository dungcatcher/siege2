import pygame
from towers import TownHall
from side_menu import SideMenu

pygame.init()

WIDTH, HEIGHT = 900, 720
TILE_SIZE = 15
menu_width = HEIGHT
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


def generate_map():
    map_surface = pygame.Surface((menu_width, HEIGHT))
    for x in range(map_surface.get_width() // TILE_SIZE):
        for y in range(map_surface.get_height() // TILE_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x + y) % 2 == 0:
                pygame.draw.rect(map_surface, (0, 255, 0), rect)
            else:
                pygame.draw.rect(map_surface, (30, 200, 30), rect)

    return map_surface


def main():
    towers = []

    clock = pygame.time.Clock()
    map_surface = generate_map()
    map_rect = map_surface.get_rect(topleft=(0, 0))
    side_menu = SideMenu((WIDTH, HEIGHT), map_surface.get_size())

    left_click = False
    town_hall_placed = False

    while True:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        WINDOW.blit(map_surface, map_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        side_menu.render(WINDOW)

        if not town_hall_placed:
            if left_click:
                if map_rect.collidepoint((mouse_x, mouse_y)):
                    tile_position = (mouse_x // TILE_SIZE, mouse_y // TILE_SIZE)
                    new_tower = TownHall(tile_position, TILE_SIZE)
                    towers.append(new_tower)
                    town_hall_placed = True

        for tower in towers:
            tower.render(WINDOW)

        left_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_click = True

        pygame.display.flip()


main()
