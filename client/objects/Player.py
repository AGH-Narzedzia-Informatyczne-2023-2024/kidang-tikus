import math

import pygame

from objects.weapons.MachineGun import MachineGun
from objects.weapons.Pistol import Pistol
from objects.weapons.Shotgun import Shotgun
from utilits.Math import Math

WEAPONCHANGECOOLDOWN = 2000
STARTHEALTH = 100
REGEN_AFTER = 7000 # 0 to disable
REGEN_RATE = 5

class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    controls = [
        {
            "up" : pygame.K_w,
            "down" : pygame.K_s,
            "left" : pygame.K_a,
            "right" : pygame.K_d,
            "switch_left" : pygame.K_q,
            "switch_right" : pygame.K_e,
            "atk" : pygame.K_SPACE
        },
        {
            "up" : pygame.K_UP,
            "down" : pygame.K_DOWN,
            "left" : pygame.K_LEFT,
            "right" : pygame.K_RIGHT,
            "switch_left" : pygame.K_LESS,
            "switch_right" : pygame.K_GREATER,
            "atk" : pygame.K_KP_ENTER
        }
    ]


    def __init__(self, pos, id, color): #id gracza do controlsów
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.weapon_pos = [self.rect.width // 2, self.rect.height // 2]
        self.pos = pos
        self.id = id
        self.maxhealth = STARTHEALTH
        self.health = self.maxhealth
        self.movementVector = [0, 0]
        self.movementSpeed = 300
        self.availableWeapons = [Pistol(),
                                 Shotgun(),
                                 MachineGun()]
        self.equippedWeapon = 0
        self.lastNonZeroMovement = [0, 0]
        self.lastWeaponChange = 0
        self.forcefieldEnd = 0
        self.forcefieldEndOnShoot = False
        self.lastDamaged = 0

    def respawn(self, pos):
        self.pos = pos
        self.health = self.maxhealth
        self.equippedWeapon = 0
        self.movementVector = [0, 0]
        self.lastNonZeroMovement = [0, 0]
        self.lastWeaponChange = 0
        self.forcefieldEnd = 0
        self.forcefieldEndOnShoot = False
        self.lastDamaged = 0

    def set_forcefield(self, time, endOnShoot = False):
        self.forcefieldEnd = pygame.time.get_ticks() + time
        self.forcefieldEndOnShoot = endOnShoot

    def is_forcefield(self):
        return pygame.time.get_ticks() < self.forcefieldEnd

    def damage(self, damage):
        if self.can_damage():
            self.health = max(self.health - damage, 0)
            self.lastDamaged = pygame.time.get_ticks()
            return True
        return False

    def can_damage(self):
        return self.is_alive() and not self.is_forcefield()

    def is_alive(self):
        return self.health > 0

    def get_health_text(self):
        return f"{int(self.health)}/{int(self.maxhealth)}"

    def move(self, screen_size, delta_time, wallsRectGenerator):
        # Regen health
        if REGEN_AFTER != 0 and pygame.time.get_ticks() - self.lastDamaged > REGEN_AFTER:
            if self.is_alive():
                self.health = min(self.health + REGEN_RATE * delta_time, self.maxhealth)

        # Movement
        self.movementVector = Math.normalize_vector(self.movementVector)
        movementDirection = Math.vector_sign(self.movementVector)

        steps = max(math.fabs(self.movementVector[0]),
                    math.fabs(self.movementVector[1])) * self.movementSpeed * delta_time
        for _ in range(int(steps)):
            for potentialNewChanges in [[1, 1], [1, 0], [0, 1]]:
                newPos = [self.pos[0] + movementDirection[0] * potentialNewChanges[0],
                          self.pos[1] + movementDirection[1] * potentialNewChanges[1]]

                if newPos[0] < 0 or newPos[0] > screen_size[0] - self.rect.width:
                    continue
                if newPos[1] < 0 or newPos[1] > screen_size[1] - self.rect.height:
                    continue
                newRect = pygame.Rect(newPos[0], newPos[1], self.rect.width, self.rect.height)

                canMove = True
                for rect in wallsRectGenerator():
                    if rect.colliderect(newRect):
                        canMove = False
                        continue

                if not canMove:
                    continue

                self.pos = newPos
                break

        self.rect.topleft = self.pos
        self.movementVector = [0, 0]

    @staticmethod
    def move_projectiles(screen_size, delta_time, wallsRectGenerator, players):
        for proj in Player.projectiles:
            proj.move(screen_size, delta_time, wallsRectGenerator, players)

    @staticmethod
    def render_projectiles(surface):
        for proj in Player.projectiles:
            proj.render(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Moved here because the weapon wouldn't switch if key isn't pressed during render step
            if len(self.availableWeapons) != 0:
                if event.key == self.controls[self.id]["switch_left"] and pygame.time.get_ticks() - self.lastWeaponChange > WEAPONCHANGECOOLDOWN:
                    self.lastWeaponChange = pygame.time.get_ticks()
                    self.equippedWeapon = (self.equippedWeapon - 1) % len(self.availableWeapons)
                elif event.key == self.controls[self.id]["switch_right"] and pygame.time.get_ticks() - self.lastWeaponChange > WEAPONCHANGECOOLDOWN:
                    self.lastWeaponChange = pygame.time.get_ticks()
                    self.equippedWeapon = (self.equippedWeapon + 1) % len(self.availableWeapons)

    def process_input(self, keys):
        if keys[self.controls[self.id]["up"]]:
            self.movementVector[1] -= 1
        if keys[self.controls[self.id]["left"]]:
            self.movementVector[0] -= 1
        if keys[self.controls[self.id]["down"]]:
            self.movementVector[1] += 1
        if keys[self.controls[self.id]["right"]]:
            self.movementVector[0] += 1
        if keys[self.controls[self.id]["atk"]]:
            self.shoot()
            if self.forcefieldEndOnShoot:
                self.forcefieldEnd = 0
                self.forcefieldEndOnShoot = False

        if self.movementVector != [0,0]:
            self.lastNonZeroMovement = self.movementVector

    def shoot(self):
        if self.lastNonZeroMovement != [0, 0] and len(self.availableWeapons) != 0:
            self.availableWeapons[self.equippedWeapon].shoot(self, self.lastNonZeroMovement, self.id)

    def render(self, surface):
        if self.is_forcefield():
            pygame.draw.circle(surface, (255, 255, 255), [self.pos[0] + 10, self.pos[1] + 10], 20, 2)
        surface.blit(self.image, self.pos)

    def get_weapon_pos(self):
        return Math.add_vectors(self.pos, self.weapon_pos)
