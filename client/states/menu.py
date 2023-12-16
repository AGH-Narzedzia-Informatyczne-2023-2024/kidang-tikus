import pygame

from state import State
from states.editor import EditorState
from states.gameselectlevel import GameSelectLevelState


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)

        self.menuSurfaceData = game.surfaces.create_surface()
        self.menuSurface = self.menuSurfaceData.surface

        self.fonts.draw_text("Kidang Tikus", (255, 255, 255), "Arial40", self.menuSurface,
                             (game.GAME_SIZE[0] / 2, 100))
        self.playText, self.playTextRect = self.fonts.draw_text("Play", (255, 255, 255), "Arial30", self.menuSurface,
                                                                (game.GAME_SIZE[0] / 2, 170))
        self.editorText, self.editorTextRect = self.fonts.draw_text("Editor", (255, 255, 255), "Arial30",
                                                                    self.menuSurface, (game.GAME_SIZE[0] / 2, 210))
        # self.fonts.draw_text("Options", (255, 255, 255), "Arial30", self.menuSurface, (game.GAME_SIZE[0] / 2, 200))
        self.exitText, self.exitTextRect = self.fonts.draw_text("Exit", (255, 255, 255), "Arial30", self.menuSurface,
                                                                (game.GAME_SIZE[0] / 2, 250))

    def cleanup(self):
        self.game.surfaces.remove_surface(self.menuSurfaceData)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.game.surfaces.get_interactive_surface(
                event.pos) == self.menuSurfaceData:  # Mouse press
                if self.playTextRect.collidepoint(event.pos):
                    self.game.open_state(GameSelectLevelState(self.game))
                    # self.game.close_state(self)  # Probably shouldn't be done if we ever want to get back to home menu screen
                if self.editorTextRect.collidepoint(event.pos):
                    self.game.open_state(EditorState(self.game))
                elif self.exitTextRect.collidepoint(event.pos):
                    self.game.running = False
