import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load('./Assets/bullet.png').convert_alpha()
        self.angle = math.atan2(self.vel[1], self.vel[0])
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 15

    def update(self, sprite_groups):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.rect.center = self.pos

        enemy_collisions = pygame.sprite.spritecollide(self, sprite_groups["enemies"], True)
        for collision in enemy_collisions:
            print('l')