import pygame

class SurfaceData():
  def __init__(self, size, zindex):
    self.surface = pygame.Surface(size)
    self.zindex = zindex

    self.pos = (0, 0)
    self.size = size
  
  def set_pos(self, pos):
    self.pos = pos

class Surfaces():
  def __init__(self, game):
    self.game = game
    self.surfaces = []

  def create_surface(self, size=(-1,-1), zindex=1):
    if size == (-1,-1):
      size = self.game.SCREEN_SIZE

    surfaceData = SurfaceData(size, zindex)

    # Insert into proper zindex
    for i in range(len(self.surfaces) + 1):
      if i == len(self.surfaces):
        self.surfaces.append(surfaceData)
      elif self.surfaces[i].zindex >= zindex:
        self.surfaces.insert(i, surfaceData)

    return surfaceData
  
  def remove_surface(self, surfaceData):
    self.surfaces.remove(surfaceData)
  
  def get_interactive_surface(self, pos):
    for i in range(len(self.surfaces) - 1, -1, -1):
      surfaceData = self.surfaces[i]
      if (surfaceData.pos[0] <= pos[0] and # X
        pos[0] <= surfaceData.pos[0] + surfaceData.size[0] and
        surfaceData.pos[1] <= pos[1] and # Y
        pos[1] <= surfaceData.pos[1] + surfaceData.size[1]):
        return surfaceData
  
  def render_surfaces(self):
    for surfaceData in self.surfaces: # Render in the zindex order
      self.game.main_canvas.blit(surfaceData.surface, surfaceData.pos)