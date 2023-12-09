import pygame

class Utils():
  def __init__(self, game):
    self.game = game

    self.fonts = {
      "Arial40": pygame.font.SysFont("Arial", 40),
      "Arial30": pygame.font.SysFont("Arial", 30)
    }
  
  def draw_text_mt(self, text, color, font, surface, position):
    textSurface = self.fonts[font].render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.midtop = position
    surface.blit(textSurface, textRect)
    return textSurface, textRect