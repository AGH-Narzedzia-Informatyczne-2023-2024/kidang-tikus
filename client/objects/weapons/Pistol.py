import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utilits.Math import Math


class Pistol(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 300
        self.damage = 35
        self.name = "Pistol"

    def shoot(self, user, movementVector, playerShooterId):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.last_shot > self.weapon_cooldown:
            direction = movementVector
            self.last_shot = currentTime
            user.projectiles.add(
                Projectile(user.get_weapon_pos(), Math.normalize_vector(direction), 500, 1500, (0, 0, 255), self.damage, [playerShooterId]))
