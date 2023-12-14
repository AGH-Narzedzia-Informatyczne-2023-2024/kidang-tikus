import pygame

from objects.Player import Player
from state import State
from states.level import Level, LevelYOffset
from states.prompt import PromptState

class GameState(State):
    def __init__(self, game, levelName):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=3)
        self.surface = self.surfaceData.surface

        self.level = Level(game)
        self.level.tilesManager.load(levelName)
        self.levelSize = self.level.get_level_size()

        self.players = [
            Player([0, 0], 0, (255, 0, 0)),
            Player([self.levelSize[0] - 50, self.levelSize[1] - 50], 1, (0, 255, 0))
        ]
        self.player_group = pygame.sprite.Group(*self.players)
        for player in self.players: # Add forcefield
            player.set_forcefield(5000, endOnShoot=True)

        self.controlsOffset = self.game.GAME_SIZE[1] - LevelYOffset
        self.exitPrompt = None

    def cleanup(self):
        self.game.surfaces.remove_surface(self.surfaceData)

    def handle_exit(self, result):
        self.exitPrompt = None
        if result:
            self.game.close_state(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.game.surfaces.get_interactive_surface(
                event.pos) == self.surfaceData:  # Mouse press
                # Exit editor
                if hasattr(self, 'exitTextRect') and self.exitTextRect.collidepoint(event.pos):
                    if self.exitPrompt is None:
                        self.exitPrompt = PromptState(self.game, "Are you sure you exit?", callback=self.handle_exit)
                        self.game.open_state(self.exitPrompt)
        for player in self.players:
            player.handle_event(event)

    def update(self):
        self.surface.fill((0, 100, 100))

        # Level
        self.level.update()

        # Players
        keys = pygame.key.get_pressed()

        for player in self.players:
            player.process_input(keys)
            player.move(self.levelSize, self.game.clock.get_time() / 1000, self.level.get_collideable_tiles_rects)

        Player.move_projectiles(self.levelSize, self.game.clock.get_time() / 1000,
                                self.level.get_collideable_tiles_rects, self.players)
        Player.render_projectiles(self.level.surface)

        for player in self.player_group.sprites():
            if player.is_alive():
                player.render(self.level.surface)

        # Text data
        self.utils.draw_text("Player 1 (RED)", (255, 255, 255), "Arial30", self.surface, (400, self.controlsOffset + 30), positionProp='midtop')
        self.utils.draw_text(f"Health: {self.players[0].get_health_text()}", (255, 255, 255), "Arial30", self.surface, (400, self.controlsOffset + 65), positionProp='midtop')
        self.utils.draw_text("Controls: WSAD QE Space", (255, 255, 255), "Arial30", self.surface, (400, self.controlsOffset + 100), positionProp='midtop')

        self.utils.draw_text("Player 2 (GREEN)", (255, 255, 255), "Arial30", self.surface, (800, self.controlsOffset + 30), positionProp='midtop')
        self.utils.draw_text(f"Health: {self.players[1].get_health_text()}", (255, 255, 255), "Arial30", self.surface, (800, self.controlsOffset + 65), positionProp='midtop')
        self.utils.draw_text("Controls: Arrow <> Enter", (255, 255, 255), "Arial30", self.surface, (800, self.controlsOffset + 100), positionProp='midtop')

        self.exitText, self.exitTextRect = self.utils.draw_text("Exit", (255, 255, 255), "Arial30", self.surface,
                                                                (25, self.game.GAME_SIZE[1] - 25),
                                                                positionProp='bottomleft')
        # Blit the level with the player
        self.surface.blit(self.level.surface, ((self.game.GAME_SIZE[0] - self.levelSize[0]) / 2, 0))
