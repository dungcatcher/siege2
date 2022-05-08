import pygame
import pygame.freetype

pygame.freetype.init()

bahnschrift = pygame.freetype.SysFont('bahnschrift', 16)

name_to_image_name = {
    "Gun Tower": "guntower",
}


class MenuItem:
    def __init__(self, pos, size, name):
        if name != "Wall":
            self.image = pygame.image.load(f'Assets/{name_to_image_name[name]}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
            self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        else:
            self.image = pygame.Surface((size, size))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(pos[0], pos[1]))
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
        item_names = ["Gun Tower", "Wall"]
        new_items = []
        for i, item_name in enumerate(item_names):
            x_pos = self.selection_rect.left + (i % 2 + 1) * (self.selection_rect.width // 3)
            y_pos = self.selection_rect.top + self.selection_rect.width // 3 + (i // 2)
            new_items.append(MenuItem((x_pos, y_pos), self.selection_rect.width * 0.25, item_name))

        return new_items

    def update(self, game):
        for item in self.items:
            if game.left_click and item.mouse_over(game.mouse_position) and game.town_hall_placed:
                game.money -= 10
                game.bought_tower = item
        self.money = game.money

    def render(self, surface):
        pygame.draw.rect(surface, (30, 30, 70), self.rect)

        money_surf, money_rect = bahnschrift.render(f'Money: {self.money}', (255, 255, 255))
        money_rect.center = (self.rect.centerx, self.rect.height * 0.05)
        surface.blit(money_surf, money_rect)

        for item in self.items:
            surface.blit(item.image, item.rect)


