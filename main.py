import pygame
from towers import TownHall

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
    clock = pygame.time.Clock()
    map_surface = generate_map()
    shit_tower = TownHall((4, 4), TILE_SIZE)

    while True:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        WINDOW.blit(map_surface, (0, 0))

        shit_tower.render(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()


main()
