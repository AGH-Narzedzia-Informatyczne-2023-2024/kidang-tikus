import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.pos = pos

    def render(self, surface):
        surface.blit(self.image, self.pos)
