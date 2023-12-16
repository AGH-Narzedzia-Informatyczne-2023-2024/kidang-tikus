import pygame

from state import State


class PromptState(State):
    def __init__(self, game, prompt, callback=None):
        super().__init__(game)

        self.size = (game.GAME_SIZE[0] / 2, game.GAME_SIZE[1] / 2)

        self.promptSurfaceData = game.surfaces.create_surface(
            size=self.size,
            zindex=10
        )
        self.promptSurfaceData.set_pos((
            (game.GAME_SIZE[0] - self.size[0]) / 2,
            (game.GAME_SIZE[1] - self.size[1]) / 2
        ))
        self.promptSurface = self.promptSurfaceData.surface

        self.utils.draw_text(prompt, (255, 255, 255), "Arial40", self.promptSurface, (self.size[0] // 2, 100))

        self.yesText, self.yesTextRect = self.utils.draw_text("Yes", (255, 255, 255), "Arial30", self.promptSurface,
                                                              (self.size[0] // 4, 175))
        self.noText, self.noTextRect = self.utils.draw_text("No", (255, 255, 255), "Arial30", self.promptSurface,
                                                            (self.size[0] * 3 // 4, 175))
        self.result = None
        self.callback = callback

    def cleanup(self):
        self.game.surfaces.remove_surface(self.promptSurfaceData)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.game.surfaces.get_interactive_surface(
                event.pos) == self.promptSurfaceData:  # Mouse press
                pos = (event.pos[0] - self.promptSurfaceData.pos[0], event.pos[1] - self.promptSurfaceData.pos[1])
                if self.yesTextRect.collidepoint(pos):
                    self.result = True
                    self.game.close_state(self)
                elif self.noTextRect.collidepoint(pos):
                    self.result = False
                    self.game.close_state(self)

                if self.result is not None:
                    self.callback(self.result)
