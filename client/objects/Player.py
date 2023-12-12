import pygame

from objects.weapons.MachineGun import MachineGun
from objects.weapons.Pistol import Pistol
from objects.weapons.Shotgun import Shotgun
from utilits.Math import Math

PLAYERCOLOR = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    movement_speed = 100

    def __init__(self, screen_size):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(PLAYERCOLOR)
        self.rect = self.image.get_rect(x=screen_size[0] // 2,
                                        y=screen_size[1] // 2)

        self.weapon_pos = [self.rect.width // 2, self.rect.height // 2]
        self.pos = [screen_size[0] // 2, screen_size[1] // 2]
        self.health = 3
        self.alive = True
        self.movementVector = [0, 0]
        self.movementSpeed = 3
        self.availableWeapons = [Pistol(),
                                 Shotgun(),
                                 MachineGun()]
        self.equippedWeapon = self.availableWeapons[0]

    def move(self, screen_size, delta_time, walls):
        self.movementVector = Math.normalize_vector(self.movementVector)

        movementDirection = Math.vector_sign(self.movementVector)

        # print(
        #     max(math.fabs(self.movementVector[0]), math.fabs(self.movementVector[1])) * self.movementSpeed * delta_time)
        for steps in range(3):
            for potentialNewChanges in [[1, 1], [1, 0], [0, 1]]:
                newPos = [self.pos[0] + movementDirection[0] * potentialNewChanges[0],
                          self.pos[1] + movementDirection[1] * potentialNewChanges[1]]

                if newPos[0] < 0 or newPos[0] > screen_size[0] - self.rect.width:
                    continue
                if newPos[1] < 0 or newPos[1] > screen_size[1] - self.rect.height:
                    continue
                newRect = pygame.Rect(newPos[0], newPos[1], self.rect.width, self.rect.height)

                canMove = True
                for wall in walls:
                    if wall.rect.colliderect(newRect):
                        canMove = False
                        continue

                if not canMove:
                    continue

                self.pos = newPos
                break

        self.rect.topleft = self.pos
        self.movementVector = [0, 0]

        for proj in Player.projectiles:
            proj.move(screen_size, delta_time, walls)

    def process_input(self, keys, mouse):
        if keys[pygame.K_w]:
            self.movementVector[1] -= 1
        if keys[pygame.K_a]:
            self.movementVector[0] -= 1
        if keys[pygame.K_s]:
            self.movementVector[1] += 1
        if keys[pygame.K_d]:
            self.movementVector[0] += 1
        if keys[pygame.K_1]:
            self.equippedWeapon = self.availableWeapons[0]
        if keys[pygame.K_2]:
            self.equippedWeapon = self.availableWeapons[1]
        if keys[pygame.K_3]:
            self.equippedWeapon = self.availableWeapons[2]
        if mouse[0]:
            self.shoot(pygame.mouse.get_pos())

    def shoot(self, mouse_pos):
        self.equippedWeapon.shoot(self, mouse_pos)

    def render(self, surface):
        surface.blit(self.image, self.pos)
        for proj in Player.projectiles:
            proj.render(surface)

    def get_weapon_pos(self):
        return Math.add_vectors(self.pos, self.weapon_pos)
