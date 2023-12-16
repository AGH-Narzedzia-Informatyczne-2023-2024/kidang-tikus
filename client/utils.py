import pygame


class Utils:
    def __init__(self, game):
        self.game = game

        self.fonts = {
            "Arial40": pygame.font.SysFont("Arial", 40),
            "Arial30": pygame.font.SysFont("Arial", 30),
            "Arial20": pygame.font.SysFont("Arial", 20),
        }

    def draw_text(self, text, color, font, surface, position, positionProp="midtop"):
        textSurface = self.fonts[font].render(text, True, color)
        textRect = textSurface.get_rect()
        setattr(textRect, positionProp, position)
        surface.blit(textSurface, textRect)
        return textSurface, textRect
