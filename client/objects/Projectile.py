import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, source, target, speed, lifetime, color):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect(x=source[0], y=source[1])
        pygame.draw.circle(self.image, color,
                           (self.rect.width // 2, self.rect.height // 2),
                           self.rect.width // 2)

        self.pos = [source[0], source[1]]
        self.movementVector = [target[0], target[1]]
        self.speed = speed
        self.lifetime = lifetime
        self.createdAt = pygame.time.get_ticks()

    def move(self, surface_size, delta_time, wallsRectGenerator):
        if pygame.time.get_ticks() > self.createdAt + self.lifetime:
            self.kill()
        self.pos[0] += self.movementVector[0] * self.speed * delta_time
        self.pos[1] += self.movementVector[1] * self.speed * delta_time
        self.rect.topleft = self.pos

        for rect in wallsRectGenerator():
            if rect.colliderect(self.rect):
                self.kill()

        if self.pos[0] > surface_size[0] or self.pos[0] < 0 or self.pos[1] > surface_size[1] or self.pos[1] < 0:
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.pos)
