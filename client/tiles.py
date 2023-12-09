import pygame
import os

class Tile():
  def __init__(self, path, speed_multiplier=1, collidable=False):
    self.surf = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
    self.rect = self.surf.get_rect()

    self.img = pygame.image.load(os.path.join(path))
    self.surf.blit(pygame.transform.scale(self.img, (50, 50)), self.rect)

    self.speed_multiplier = speed_multiplier
    self.collidable = collidable

BricksTile = Tile("assets/tiles/bricks.png")
DarkBricksTile = Tile("assets/tiles/dark_bricks.png")
DarkBricks2Tile = Tile("assets/tiles/dark_bricks2.png")
DiamondOreTile = Tile("assets/tiles/diamond_ore.png")
DirtyBricksTile = Tile("assets/tiles/dirty_bricks.png")
GrassTile = Tile("assets/tiles/grass.png")
LavaTile = Tile("assets/tiles/lava.png")
LogTile = Tile("assets/tiles/log.png")
MessyBricksTile = Tile("assets/tiles/messy_bricks.png")
SandTile = Tile("assets/tiles/sand.png")
StoneTile = Tile("assets/tiles/stone.png")
WaterTile = Tile("assets/tiles/water.png")

TileDict = {
  "Bricks": BricksTile,
  "DarkBricks": DarkBricksTile,
  "DarkBricks2": DarkBricks2Tile,
  "DiamondOre": DiamondOreTile,
  "DirtyBricks": DirtyBricksTile,
  "Grass": GrassTile,
  "Lava": LavaTile,
  "Log": LogTile,
  "MessyBricks": MessyBricksTile,
  "Sand": SandTile,
  "Stone": StoneTile,
  "Water": WaterTile,
}