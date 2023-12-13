import pygame
import re
import os

from tiles import TileDict

LevelYOffset = 150
Extension = ".kiti"

class TileData():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tileName = None

  def is_at(self, x, y):
    return self.x == x and self.y == y

  def set_tile(self, tileName):
    self.tileName = tileName

class TilesManager():
  def __init__(self):
    self.tiles = []

  def find(self, x, y):
    for i in range(len(self.tiles)):
      if self.tiles[i].is_at(x, y):
        return i
    return None

  def change(self, x, y, tileName = None):
    i = self.find(x, y)
    if i == None:
      if tileName != None:
        tileData = TileData(x, y)
        tileData.set_tile(tileName)
        self.tiles.append(tileData)
    else:
      if tileName == None:
        del self.tiles[i]
      else:
        self.tiles[i].set_tile(tileName)

  def validateName(self, name):
    if len(name) <= 3 or len(name) > 20:
      return False

    # Only allow alphanumeric characters, spaces and underscores
    result = re.search("^[a-zA-Z0-9 _]+$", name)
    if result == None:
      return False

    return True

  def clear(self):
    self.tiles.clear()

  def save(self, name):
    if (not self.validateName(name)):
      return False

    try:
      with open(os.path.join("client/saves", name + Extension), "w") as file:
        file.write("1\n") # Version (placeholder)
        for tile in self.tiles:
          file.write(str(tile.x) + "," + str(tile.y) + ":" + tile.tileName + ";")
      return True
    except IOError as e:
      print("Save failed: ", e)
    return False

  def load(self, name):
    if (not self.validateName(name)):
      return False

    try:
      with open(os.path.join("client/saves", name + Extension), "r") as file:
        (version, tiles) = file.read().split("\n")
        tiles = tiles.split(";")
        self.clear()
        for tile in tiles:
          if len(tile) == 0:
            continue
          (pos, tileName) = tile.split(":")
          (x, y) = pos.split(",")
          self.change(int(x), int(y), tileName)
        return True
    except IOError as e:
      print("Load failed: ", e)
      return False

  @staticmethod
  def getSaveList():
    saves = []
    for file in os.listdir("client/saves"):
      if file.endswith(Extension):
        saves.append(file[:-len(Extension)])
    return saves

class Level():
  def __init__(self, game):
    self.surface = pygame.Surface(
      (game.GAME_SIZE[0], game.GAME_SIZE[1] - LevelYOffset),
      pygame.SRCALPHA, 32)
    self.tilesManager = TilesManager()

  def get_collideable_tiles_rects(self):
    for tile in self.tilesManager.tiles:
      if TileDict[tile.tileName].collidable:
        yield pygame.Rect(tile.x * 50, tile.y * 50, 50, 50)

  def get_level_size(self):
    levelSize = [0, 0]
    for tile in self.tilesManager.tiles:
      if (tile.x + 1) * 50 > levelSize[0]:
        levelSize[0] = (tile.x + 1) * 50
      if (tile.y + 1) * 50 > levelSize[1]:
        levelSize[1] = (tile.y + 1) * 50
    return levelSize

  def update(self):
    self.surface.fill((0,0,0,0))

    # Render the tiles
    for tile in self.tilesManager.tiles:
      tileSurface = TileDict[tile.tileName].surf
      self.surface.blit(tileSurface, (tile.x * 50, tile.y * 50))
