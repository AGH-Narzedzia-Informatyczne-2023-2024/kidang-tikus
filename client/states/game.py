import pygame

from components.level import Level, LevelYOffset
from objects.Player import Player
from state import State
from states.prompt import PromptState

RESPAWN_DELAY = 1500
FORCEFIELD_TIME = 5000
FORCEFIELD_END_ON_SHOOT = True


class GameState(State):
    def __init__(self, game, levelName):
        super().__init__(game)

        self.surfaceData = game.surfaces.create_surface(zindex=3)
        self.surface = self.surfaceData.surface

        self.level = Level(game)
        self.level.tilesManager.load(levelName)
        self.levelSize = self.level.get_level_size()

        self.initialPlayerPositions = [
            [0, 0],
            [self.levelSize[0] - 50, self.levelSize[1] - 50]
        ]
        self.playerColors = [
            (100, 0, 0),
            (0, 100, 0)
        ]

        self.players = []
        for i in range(2):
            self.players.append(Player(self.initialPlayerPositions[i], i, self.playerColors[i]))

        self.player_group = pygame.sprite.Group(*self.players)
        for player in self.players:  # Add forcefield
            player.set_forcefield(FORCEFIELD_TIME, endOnShoot=FORCEFIELD_END_ON_SHOOT)

        self.controlsOffset = self.game.GAME_SIZE[1] - LevelYOffset
        self.exitPrompt = None

        self.scores = [0, 0]
        self.canScore = [True, True]

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
        self.surface.fill((0, 0, 0))

        # Level
        self.level.update()

        # Players
        keys = pygame.key.get_pressed()

        for player in self.players:
            player.process_input(keys)
            player.move(self.levelSize, self.game.clock.get_time() / 1000, self.level.get_collideable_tiles_rects)

            if not player.is_alive():  # Handling points and respawning
                scoringPlayer = 1 - player.id
                if self.canScore[scoringPlayer]:
                    self.canScore[scoringPlayer] = False
                    self.scores[scoringPlayer] += 1

                if RESPAWN_DELAY != 0:
                    if player.lastDamaged + RESPAWN_DELAY < pygame.time.get_ticks():
                        player.respawn(self.initialPlayerPositions[player.id])
                        self.canScore[scoringPlayer] = True
                        player.set_forcefield(FORCEFIELD_TIME, endOnShoot=FORCEFIELD_END_ON_SHOOT)

        Player.move_projectiles(self.levelSize, self.game.clock.get_time() / 1000,
                                self.level.get_collideable_tiles_rects, self.players)
        Player.render_projectiles(self.level.surface)

        for player in self.player_group.sprites():
            if player.is_alive():
                player.render(self.level.surface)

        # Text data
        self.fonts.draw_text(f"{self.scores[0]}:{self.scores[1]}", (255, 255, 255), "Arial40", self.surface,
                             (self.game.GAME_SIZE[0] / 2, self.controlsOffset + 5), positionProp='midtop')

        self.fonts.draw_text("Player 1 (RED)", (255, 255, 255), "Arial30", self.surface,
                             (400, self.controlsOffset + 20), positionProp='midtop')
        self.fonts.draw_text(f"Health: {self.players[0].get_health_text()}", (255, 255, 255), "Arial20", self.surface,
                             (400, self.controlsOffset + 60), positionProp='midtop')
        self.fonts.draw_text(f"Weapon: {self.players[0].get_weapon_name()}", (255, 255, 255), "Arial20", self.surface,
                             (400, self.controlsOffset + 85), positionProp='midtop')
        self.fonts.draw_text("Controls: WSAD QE Space", (255, 255, 255), "Arial20", self.surface,
                             (400, self.controlsOffset + 110), positionProp='midtop')

        self.fonts.draw_text("Player 2 (GREEN)", (255, 255, 255), "Arial30", self.surface,
                             (800, self.controlsOffset + 20), positionProp='midtop')
        self.fonts.draw_text(f"Health: {self.players[1].get_health_text()}", (255, 255, 255), "Arial20", self.surface,
                             (800, self.controlsOffset + 60), positionProp='midtop')
        self.fonts.draw_text(f"Weapon: {self.players[1].get_weapon_name()}", (255, 255, 255), "Arial20", self.surface,
                             (800, self.controlsOffset + 85), positionProp='midtop')
        self.fonts.draw_text("Controls: Arrow <> Enter", (255, 255, 255), "Arial20", self.surface,
                             (800, self.controlsOffset + 110), positionProp='midtop')

        self.exitText, self.exitTextRect = self.fonts.draw_text("Exit", (255, 255, 255), "Arial30", self.surface,
                                                                (25, self.game.GAME_SIZE[1] - 25),
                                                                positionProp='bottomleft')
        # Blit the level with the player
        self.surface.blit(self.level.surface, ((self.game.GAME_SIZE[0] - self.levelSize[0]) / 2, 0))
