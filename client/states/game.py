import pygame

from objects.Player import Player
from state import State
from states.level import Level


class GameState(State):
    def __init__(self, game, levelName):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=3)
        self.surface = self.surfaceData.surface

        self.level = Level(game)
        self.level.tilesManager.load(levelName)
        self.levelSize = self.level.get_level_size()

        self.players = [
            Player([0, 0]),
            Player([self.levelSize[0] - 50, self.levelSize[1] - 50])
        ]
        self.player_group = pygame.sprite.Group(*self.players)

    def update(self):
        self.surface.fill((0, 100, 100))

        # Level
        self.level.update()

        # Players
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        for player in self.players:
            player.process_input(keys, mouse)  # Need to replace mouse with sth else
            player.move(self.levelSize, self.game.clock.get_time() / 1000, self.level.get_collideable_tiles_rects)

        Player.move_projectiles(self.levelSize, self.game.clock.get_time() / 1000,
                                self.level.get_collideable_tiles_rects)

        for sprite in self.player_group.sprites():
            sprite.render(self.level.surface)

        # Blit the level with the player
        self.surface.blit(self.level.surface, ((self.game.GAME_SIZE[0] - self.levelSize[0]) / 2, 0))
