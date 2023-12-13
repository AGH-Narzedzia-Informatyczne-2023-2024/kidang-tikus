import pygame

from state import State
from states.game import GameState
from states.level import TilesManager


class GameSelectLevelState(State):
    def __init__(self, game):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=3)
        self.surface = self.surfaceData.surface

        self.utils.draw_text("Pick the level", (255, 255, 255), "Arial40", self.surface,
                             (game.GAME_SIZE[0] / 2, 100))
        self.levelsList = TilesManager.getSaveList()
        self.levelsRects = []
        i = 0
        for level in self.levelsList:
            text, rect = self.utils.draw_text(level, (255, 255, 255), "Arial30", self.surface,
                                              (game.GAME_SIZE[0] / 2, 170 + i * 40))
            self.levelsRects.append((level, rect))
            i += 1

        self.backText, self.backTextRect = self.utils.draw_text("Back", (255, 255, 255), "Arial30", self.surface,
                                                                (game.GAME_SIZE[0] / 2, 170 + i * 40))

    def cleanup(self):
        self.game.surfaces.remove_surface(self.surfaceData)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.game.surfaces.get_interactive_surface(
                event.pos) == self.surfaceData:  # Mouse press
                if self.backTextRect.collidepoint(event.pos):
                    self.game.close_state(self)
                else:
                    for data in self.levelsRects:
                        if data[1].collidepoint(event.pos):
                            self.game.open_state(GameState(self.game, data[0]))
                            self.game.close_state(self)
