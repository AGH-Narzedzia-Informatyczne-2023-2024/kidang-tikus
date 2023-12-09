import pygame

from objects.Player import Player
from state import State


class GameState(State):
    def __init__(self, game):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=2)
        self.surface = self.surfaceData.surface

        self.player = Player(game.screen.get_size())
        self.player_group = pygame.sprite.GroupSingle(self.player)

    def update(self):
        self.surface.fill((0, 100, 100))

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        self.player.process_input(keys, mouse)

        self.player.move(self.game.screen.get_size(), self.game.clock.get_time() / 1000)

        self.player_group.sprite.render(self.surface)
