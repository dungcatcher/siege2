import pygame
import math


class Projectile:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load('./Assets/bullet.png').convert_alpha()
        self.angle = math.atan2(self.vel[1], self.vel[0])
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 5

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = self.pos