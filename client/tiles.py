import pygame

from utilits.path import get_assets_path


class Tile:
    def __init__(self, path, speed_multiplier=1, collidable=False):
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        self.rect = self.surf.get_rect()

        self.img = pygame.image.load(get_assets_path(path))
        self.surf.blit(pygame.transform.scale(self.img, (50, 50)), self.rect)

        self.speed_multiplier = speed_multiplier
        self.collidable = collidable


BricksTile = Tile("tiles/bricks.png")
DarkBricksTile = Tile("tiles/dark_bricks.png")
DarkBricks2Tile = Tile("tiles/dark_bricks2.png")
DiamondOreTile = Tile("tiles/diamond_ore.png")
DirtyBricksTile = Tile("tiles/dirty_bricks.png")
GrassTile = Tile("tiles/grass.png")
LavaTile = Tile("tiles/lava.png")
LogTile = Tile("tiles/log.png")
MessyBricksTile = Tile("tiles/messy_bricks.png")
SandTile = Tile("tiles/sand.png")
StoneTile = Tile("tiles/stone.png")
WaterTile = Tile("tiles/water.png")

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

# TODO: Custom order of the tiles?
TileList = []
for (key, value) in TileDict.items():
    TileList.append((key, value))
