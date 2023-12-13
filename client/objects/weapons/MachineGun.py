import math
import random

import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utilits.Math import Math


class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 50
        self.spread_arc = 5

    def shoot(self, user, movementDirection):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = movementDirection
            self.last_shot = current_time
            theta = math.radians(random.random() * self.spread_arc - self.spread_arc / 2)
            proj_dir = Math.rotate_vector(direction, theta)
            user.projectiles.add(
                Projectile(user.get_weapon_pos(), Math.normalize_vector(proj_dir), 600, 2000, (194, 54, 16)))
