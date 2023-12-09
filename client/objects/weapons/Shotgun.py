import math
import random

import pygame

from objects.Projectile import Projectile
from objects.Weapon import Weapon
from utilits.Math import Math


class Shotgun(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 800
        self.spread_arc = 30
        self.projectiles_count = 20

    def shoot(self, user, mouse_pos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.last_shot > self.weapon_cooldown:
            direction = (mouse_pos[0] - user.pos[0], mouse_pos[1] - user.pos[1]) \
                if mouse_pos != user.pos else (1, 1)
            self.last_shot = currentTime
            # arcDifference = self.spread_arc / (self.projectiles_count - 1)
            for proj in range(self.projectiles_count):
                theta = math.radians(random.random() * self.spread_arc - self.spread_arc / 2)
                projDir = Math.rotate_vector(direction, theta)
                user.projectiles.add(
                    Projectile(user.get_weapon_pos(), Math.normalize_vector(projDir), random.randrange(650, 750),
                               random.randrange(250, 550),
                               (232, 144, 42)))
