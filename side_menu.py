import pygame
import pygame.freetype
from towers import GunTower

pygame.freetype.init()

bahnschrift = pygame.freetype.SysFont('bahnschrift', 16)


class MenuItem:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def mouse_over(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            return True
        return False


class SideMenu:
    def __init__(self, screen_size, map_size, money):
        self.rect = pygame.Rect(map_size[0], 0, (screen_size[0] - map_size[0]), screen_size[1])
        self.selection_rect = pygame.Rect(self.rect.left, self.rect.height * 0.12, self.rect.width, self.rect.height * 0.88)
        self.money = money
        self.items = self.create_items()

    def create_items(self):
        item_names = ["Gun Tower", "Gun Tower"]
        new_items = []
        for i, item_name in enumerate(item_names):
            x_pos = self.selection_rect.left + (i % 2 + 1) * (self.selection_rect.width // 3)
            y_pos = self.selection_rect.top + self.selection_rect.width // 3 + (i // 2)
            if item_name == "Gun Tower":
                image = pygame.Surface((self.selection_rect.width * 0.25, self.selection_rect.width * 0.25))
                image.fill((255, 0, 0))
                rect = image.get_rect(center=(x_pos, y_pos))
                new_items.append(MenuItem(image, rect))

        return new_items

    def update(self, left_click, mouse_position):
        for item in self.items:
            if left_click and item.mouse_over(mouse_position):
                print(item.image)

    def render(self, surface):
        pygame.draw.rect(surface, (30, 30, 70), self.rect)

        money_surf, money_rect = bahnschrift.render(f'Money: {self.money}', (255, 255, 255))
        money_rect.center = (self.rect.centerx, self.rect.height * 0.05)
        surface.blit(money_surf, money_rect)

        for item in self.items:
            surface.blit(item.image, item.rect)


