import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load('./Assets/bullet.png').convert_alpha()
        self.angle = math.atan2(self.vel[1], -self.vel[0])
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 15
        self.damage = 10

    def update(self, game, sprite_groups):
        pass


class Bullet(Projectile):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.speed = 15
        self.damage = 10

    def update(self, game, sprite_groups):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.rect.center = self.pos

        #  Check collisions with enemies and kill enemy and projectile
        enemy_collisions = pygame.sprite.spritecollide(self, sprite_groups["enemies"], dokill=False)
        if enemy_collisions:
            sprite_groups["projectiles"].remove(self)
            for enemy in enemy_collisions:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.kill()
                    game.money += enemy.worth

        if not self.rect.colliderect(game.map_rect):
            self.kill()


class Bomb(Projectile):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.speed = 5
        self.damage = 25
        self.aoe = 3

    def update(self, game, sprite_groups):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.rect.center = self.pos

        #  Check collisions with enemies and kill enemy and projectile
        enemy_collisions = pygame.sprite.spritecollide(self, sprite_groups["enemies"], dokill=False)
        if enemy_collisions:
            sprite_groups["projectiles"].remove(self)
            for enemy in game.sprite_groups["enemies"]:
                distance = math.hypot(self.rect.x - enemy.rect.x, self.rect.y - enemy.rect.y)
                if distance <= self.aoe * game.tile_size:
                    tile_distance = distance / game.tile_size
                    damage = self.damage * (1 - (tile_distance / self.aoe))
                    enemy.health -= damage
                    if enemy.health <= 0:
                        enemy.kill()
                        game.money += enemy.worth

        if not self.rect.colliderect(game.map_rect):
            self.kill()
