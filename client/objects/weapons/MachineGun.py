import math
import random

import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utils.Math import Math
from utils.path import get_assets_path


class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 50
        self.spread_arc = 5
        self.damage = 4
        self.name = "Machine Gun"
        self.img = pygame.image.load(get_assets_path("rifle.png"))

    def shoot(self, user, movementDirection, playerShooterId):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = movementDirection
            self.last_shot = current_time
            theta = math.radians(random.random() * self.spread_arc - self.spread_arc / 2)
            proj_dir = Math.rotate_vector(direction, theta)
            user.projectiles.add(
                Projectile(user.get_weapon_pos(), Math.normalize_vector(proj_dir), 600, 2000, (194, 54, 16),
                           self.damage, [playerShooterId]))
