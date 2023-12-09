import pygame
from state import State

from .editor import EditorState

class MenuState(State):
  def __init__(self, game):
    super().__init__(game)

    self.menuSurfaceData = game.surfaces.create_surface()
    self.menuSurface = self.menuSurfaceData.surface

    self.utils.draw_text("Kidang Tikus", (255, 255, 255), "Arial40", self.menuSurface, (game.SCREEN_SIZE[0] / 2, 100))
    self.utils.draw_text("Play", (255, 255, 255), "Arial30", self.menuSurface, (game.SCREEN_SIZE[0] / 2, 170))
    self.editorText, self.editorTextRect = self.utils.draw_text("Editor", (255, 255, 255), "Arial30", self.menuSurface, (game.SCREEN_SIZE[0] / 2, 210))
    # self.utils.draw_text("Options", (255, 255, 255), "Arial30", self.menuSurface, (game.SCREEN_SIZE[0] / 2, 200))
    self.exitText, self.exitTextRect = self.utils.draw_text("Exit", (255, 255, 255), "Arial30", self.menuSurface, (game.SCREEN_SIZE[0] / 2, 250))
  
  def cleanup(self):
    self.game.surfaces.remove_surface(self.menuSurfaceData)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1 and self.game.surfaces.get_interactive_surface(event.pos) == self.menuSurfaceData: # Mouse press
        if self.editorTextRect.collidepoint(event.pos):
          self.game.open_state(EditorState(self.game))
        elif self.exitTextRect.collidepoint(event.pos):
          self.game.running = False