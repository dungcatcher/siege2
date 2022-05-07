import pygame
import pygame.freetype
from towers import GunTower

pygame.freetype.init()

bahnschrift = pygame.freetype.SysFont('bahnschrift', 16)


class MenuItem:
    def __init__(self, image, rect, name):
        self.image = image
        self.rect = rect
        self.name = name

    def mouse_over(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            return True
        return False


class SideMenu:
    def __init__(self, screen_size, map_size):
        self.rect = pygame.Rect(map_size[0], 0, (screen_size[0] - map_size[0]), screen_size[1])
        self.selection_rect = pygame.Rect(self.rect.left, self.rect.height * 0.12, self.rect.width, self.rect.height * 0.88)
        self.items = self.create_items()
        self.money = 500

    def create_items(self):
        item_names = ["Gun Tower", "Gun Tower"]
        new_items = []
        for i, item_name in enumerate(item_names):
            x_pos = self.selection_rect.left + (i % 2 + 1) * (self.selection_rect.width // 3)
            y_pos = self.selection_rect.top + self.selection_rect.width // 3 + (i // 2)
            if item_name == "Gun Tower":
                image = pygame.image.load('Assets/guntower.png').convert_alpha()
                image = pygame.transform.scale(image, (self.selection_rect.width * 0.25, self.selection_rect.width * 0.25))
                rect = image.get_rect(center=(x_pos, y_pos))
                new_items.append(MenuItem(image, rect, item_name))

        return new_items

    def update(self, game):
        for item in self.items:
            if game.left_click and item.mouse_over(game.mouse_position) and game.town_hall_placed:
                game.money -= 10
                self.money = game.money
                game.bought_tower = item

    def render(self, surface):
        pygame.draw.rect(surface, (30, 30, 70), self.rect)

        money_surf, money_rect = bahnschrift.render(f'Money: {self.money}', (255, 255, 255))
        money_rect.center = (self.rect.centerx, self.rect.height * 0.05)
        surface.blit(money_surf, money_rect)

        for item in self.items:
            surface.blit(item.image, item.rect)


