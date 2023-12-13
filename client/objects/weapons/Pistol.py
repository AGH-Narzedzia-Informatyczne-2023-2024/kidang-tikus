import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utilits.Math import Math


class Pistol(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 300

    def shoot(self, user, mousePos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.last_shot > self.weapon_cooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.last_shot = currentTime
            user.projectiles.add(
                Projectile(user.get_weapon_pos(), Math.normalize_vector(direction), 500, 1500, (0, 0, 255)))
