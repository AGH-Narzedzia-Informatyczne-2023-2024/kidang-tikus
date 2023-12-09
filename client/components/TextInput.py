import pygame

UnderscoreAnimFrames = 30
UnderscoreAnimInterval = UnderscoreAnimFrames * 2

class TextInput():
  def __init__(self, game, size, maxchars=-1, initialText=""):
    self.text = initialText
    self.active = False
    self.game = game
    self.size = size

    self.maxchars = maxchars

    self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    self.ticks = 0
  
  def update(self):
    self.surface.fill((0,0,0,0))

    pygame.draw.rect(self.surface, (255,255,255), (0,0,self.surface.get_width(),self.surface.get_height()), 2)
    
    self.ticks = (self.ticks + 1) % UnderscoreAnimInterval
    text = self.text
    if self.ticks < UnderscoreAnimFrames and self.active:
      text += "_"

    self.game.utils.draw_text(text, (255,255,255), "Arial30", self.surface, (10,self.size[1]//2), positionProp='midleft')
  
  def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
      if self.active:
        if event.key == pygame.K_BACKSPACE:
          self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
          self.active = False
        else:
          if self.maxchars == -1 or len(self.text) < self.maxchars:
            self.text += event.unicode
  
  def set_active(self, active):
    self.active = active

  def get_value(self):
    return self.text