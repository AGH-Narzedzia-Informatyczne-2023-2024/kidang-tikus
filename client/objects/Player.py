import math

import pygame

from objects.weapons.MachineGun import MachineGun
from objects.weapons.Pistol import Pistol
from objects.weapons.Shotgun import Shotgun
from utilits.Math import Math

PLAYERCOLOR = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    controls = [
        {
           "up" : pygame.K_w,
           "down" : pygame.K_s,
           "left" : pygame.K_a,
           "right" : pygame.K_d,
           "w1" : pygame.K_1,
           "w2" : pygame.K_2,
           "w3" : pygame.K_3,
           "atk" : pygame.K_SPACE
        },
        {
            "up" : pygame.K_UP,
           "down" : pygame.K_DOWN,
           "left" : pygame.K_LEFT,
           "right" : pygame.K_RIGHT,
           "w1" : pygame.K_8,
           "w2" : pygame.K_9,
           "w3" : pygame.K_0,
           "atk" : pygame.K_RSHIFT 
        }
    ]
        

    def __init__(self, pos, id): #id gracza do controlsów
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(PLAYERCOLOR)
        self.rect = self.image.get_rect()
        
        

        self.weapon_pos = [self.rect.width // 2, self.rect.height // 2]
        self.pos = pos
        self.id = id
        self.lastNonZero = [1-self.id*2, 0]
        self.health = 3
        self.alive = True
        self.movementVector = [0, 0]
        self.movementSpeed = 300
        self.availableWeapons = [Pistol(),
                                 Shotgun(),
                                 MachineGun()]
        self.equippedWeapon = self.availableWeapons[0]

    def move(self, screen_size, delta_time, wallsRectGenerator):
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
    def move_projectiles(screen_size, delta_time, wallsRectGenerator):
        for proj in Player.projectiles:
            proj.move(screen_size, delta_time, wallsRectGenerator)

    def process_input(self, keys, mouse):
        
        if keys[self.controls[self.id]["up"]]:
            self.movementVector[1] -= 1
        if keys[self.controls[self.id]["left"]]:
            self.movementVector[0] -= 1
        if keys[self.controls[self.id]["down"]]:
            self.movementVector[1] += 1
        if keys[self.controls[self.id]["right"]]:
            self.movementVector[0] += 1
        if keys[self.controls[self.id]["w1"]]:
            self.equippedWeapon = self.availableWeapons[0]
        if keys[self.controls[self.id]["w2"]]:
            self.equippedWeapon = self.availableWeapons[1]
        if keys[self.controls[self.id]["w3"]]:
            self.equippedWeapon = self.availableWeapons[2]
        if keys[self.controls[self.id]["atk"]]:
            self.shoot(self.movementVector)
        
        if self.movementVector != [0,0]:
            self.lastNonZero = self.movementVector

    def shoot(self, movementVector):
        if movementVector == [0, 0]:
            dir = self.lastNonZero
        else:
            dir = movementVector

        self.equippedWeapon.shoot(self, dir) 

    def render(self, surface):
        surface.blit(self.image, self.pos)
        for proj in Player.projectiles:
            proj.render(surface)

    def get_weapon_pos(self):
        return Math.add_vectors(self.pos, self.weapon_pos)
