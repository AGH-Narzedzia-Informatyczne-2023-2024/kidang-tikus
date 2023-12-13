import pygame

from objects.Player import Player
from state import State
from .level import Level


class GameState(State):
    def __init__(self, game, levelName):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=3)
        self.surface = self.surfaceData.surface

        self.level = Level(game)
        self.level.tilesManager.load(levelName)
        self.levelSize = self.level.get_level_size()

        self.player = Player(self.levelSize, [0,0])
        self.player_group = pygame.sprite.GroupSingle(self.player)

    def update(self):
        self.surface.fill((0, 100, 100))

        # Level
        self.level.update()

        # Players
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        self.player.process_input(keys, mouse) # Need to replace mouse with sth else
        self.player.move(self.levelSize, self.game.clock.get_time() / 1000, self.level.get_collideable_tiles_rects)
        self.player_group.sprite.render(self.level.surface)

        # Blit the level with the player
        self.surface.blit(self.level.surface, ((self.game.GAME_SIZE[0] - self.levelSize[0]) / 2, 0))
