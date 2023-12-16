import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utils.Math import Math
from utils.path import get_assets_path


class Pistol(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 300
        self.damage = 35
        self.name = "Pistol"
        self.img = pygame.image.load(get_assets_path("handgun.png"))

    def shoot(self, user, movementVector, playerShooterId):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.last_shot > self.weapon_cooldown:
            direction = movementVector
            self.last_shot = currentTime
            user.projectiles.add(
                Projectile(user.get_weapon_pos(), Math.normalize_vector(direction), 500, 1500, (0, 0, 255), self.damage,
                           [playerShooterId]))
