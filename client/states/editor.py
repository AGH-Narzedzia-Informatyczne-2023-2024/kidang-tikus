import pygame

from components.TextInput import TextInput
from state import State
from states.level import Level, LevelYOffset
from states.prompt import PromptState
from tiles import TileDict, TileList

SelectTilesShown = 5


class Selector(pygame.sprite.Sprite):
    def __init__(self):
        super(Selector, self).__init__()

        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect()
        self.tileName = None
        self.tileSurf = None

        self.update()

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        if self.tileSurf is not None:
            self.surf.blit(self.tileSurf, (0, 0))
        pygame.draw.rect(self.surf, (255, 255, 255), self.rect, 1)

    def set_tile(self, tileName=None):
        self.tileName = tileName
        if tileName is None:
            self.tileSurf = None
        else:
            tileSurface = TileDict[tileName].surf.copy()
            tileSurface.set_alpha(128)
            self.tileSurf = tileSurface
        self.update()


class EditorState(State):
    def __init__(self, game):
        super().__init__(game)

        self.editorSurfaceData = game.surfaces.create_surface(zindex=2)
        self.editorSurface = self.editorSurfaceData.surface
        self.tileSelector = Selector()
        self.currentTilePos = (0, 0)

        self.tileSelectIndex = 0
        self.tileSelectRects = []  # [(Rect, tileName), ...]
        self.controlsOffset = self.game.GAME_SIZE[1] - LevelYOffset

        self.level = Level(game)
        self.nameInput = TextInput(game, (300, 50), maxchars=18)

        self.exitPrompt = None

        self.loadsaveMsg = None

    def cleanup(self):
        self.game.surfaces.remove_surface(self.editorSurfaceData)

    def handle_exit(self, result):
        self.exitPrompt = None
        if result:
            self.game.close_state(self)

    def handle_event(self, event):
        self.nameInput.handle_event(event)
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] >= self.game.GAME_SIZE[0] or event.pos[1] >= self.game.GAME_SIZE[1] - LevelYOffset:
                self.currentTilePos = None
            else:
                self.currentTilePos = (event.pos[0] // 50, event.pos[1] // 50)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.nameInput.set_active(False)  # Drop focus
            self.loadsaveMsg = None  # Defer clearing?

            if event.button == 1 and self.game.surfaces.get_interactive_surface(
                event.pos) == self.editorSurfaceData:  # Mouse press
                # Switch tiles left / right
                if hasattr(self, 'leftTextRect') and self.leftTextRect.collidepoint(event.pos):
                    self.tileSelectIndex = max(self.tileSelectIndex - 1, 0)
                elif hasattr(self, 'rightTextRect') and self.rightTextRect.collidepoint(event.pos):
                    self.tileSelectIndex = min(self.tileSelectIndex + 1, len(TileList) - SelectTilesShown)
                # Delete tile
                elif hasattr(self, 'deleteTextRect') and self.deleteTextRect.collidepoint(event.pos):
                    self.tileSelector.set_tile(None)
                # Exit editor
                elif hasattr(self, 'exitTextRect') and self.exitTextRect.collidepoint(event.pos):
                    if self.exitPrompt is None:
                        self.exitPrompt = PromptState(self.game, "Are you sure you exit?", callback=self.handle_exit)
                        self.game.open_state(self.exitPrompt)
                # Select name text input
                elif hasattr(self, 'nameInputRect') and self.nameInputRect.collidepoint(event.pos):
                    self.nameInput.set_active(True)
                # Load / Save
                elif hasattr(self, 'saveTextRect') and self.saveTextRect.collidepoint(event.pos):
                    result = self.level.tilesManager.save(self.nameInput.get_value())
                    self.loadsaveMsg = "Saved" if result else "Save fail"
                elif hasattr(self, 'loadTextRect') and self.loadTextRect.collidepoint(event.pos):
                    result = self.level.tilesManager.load(self.nameInput.get_value())
                    self.loadsaveMsg = "Loaded" if result else "Load fail"
                # Place tile
                elif self.currentTilePos is not None:  # Tile placement
                    self.level.tilesManager.change(self.currentTilePos[0], self.currentTilePos[1],
                                                   self.tileSelector.tileName)
                else:
                    # Tile selection
                    for tileSelectRect in self.tileSelectRects:
                        if tileSelectRect[0].collidepoint(event.pos):
                            self.tileSelector.set_tile(tileSelectRect[1])
                            break

    def update(self):
        self.editorSurface.fill((0, 0, 0))  # Clean the surface

        # Level
        self.level.update()
        self.editorSurface.blit(self.level.surface, (0, 0))

        # Cursor
        if self.currentTilePos is not None:
            self.editorSurface.blit(self.tileSelector.surf, (self.currentTilePos[0] * 50, self.currentTilePos[1] * 50))

        # Controls
        self.exitText, self.exitTextRect = self.utils.draw_text("Exit", (255, 255, 255), "Arial30", self.editorSurface,
                                                                (25, self.game.GAME_SIZE[1] - 25),
                                                                positionProp='bottomleft')
        self.deleteText, self.deleteTextRect = self.utils.draw_text("Delete", (255, 255, 255), "Arial30",
                                                                    self.editorSurface,
                                                                    (200, self.game.GAME_SIZE[1] - 25),
                                                                    positionProp='bottomleft')
        if self.tileSelectIndex != 0:
            self.leftText, self.leftTextRect = self.utils.draw_text("<", (255, 255, 255), "Arial30", self.editorSurface,
                                                                    (50, self.controlsOffset + 50),
                                                                    positionProp='midright')
        if self.tileSelectIndex < len(TileList) - SelectTilesShown:
            self.rightText, self.rightTextRect = self.utils.draw_text(">", (255, 255, 255), "Arial30",
                                                                      self.editorSurface, (60 + SelectTilesShown * 60,
                                                                                           self.controlsOffset + 50),
                                                                      positionProp='midleft')

        self.saveText, self.saveTextRect = self.utils.draw_text("Save", (255, 255, 255), "Arial30", self.editorSurface,
                                                                (800, self.controlsOffset + 30), positionProp='topleft')
        self.loadText, self.loadTextRect = self.utils.draw_text("Load", (255, 255, 255), "Arial30", self.editorSurface,
                                                                (870, self.controlsOffset + 30), positionProp='topleft')

        if self.loadsaveMsg is not None:
            self.utils.draw_text(self.loadsaveMsg, (255, 255, 255), "Arial30", self.editorSurface,
                                 (730, self.game.GAME_SIZE[1] - 25), positionProp='bottomleft')

        self.nameInput.update()
        self.nameInputRect = self.editorSurface.blit(self.nameInput.surface, (475, self.controlsOffset + 25))

        # Tile selector
        newTileSelectRects = []
        for i in range(self.tileSelectIndex, self.tileSelectIndex + SelectTilesShown):
            if i < len(TileList):
                tile = TileList[i]
                tileRect = self.editorSurface.blit(tile[1].surf,
                                                   (60 + (i - self.tileSelectIndex) * 60, self.controlsOffset + 25))
                newTileSelectRects.append((tileRect, tile[0]))
        self.tileSelectRects.clear()
        self.tileSelectRects.extend(newTileSelectRects)
