from enum import Enum
from pyglet.sprite import Sprite


class TileType(Enum):
    Empty = 0
    Floor0 = 1
    Wall0 = 2
    Carpet0 = 3


class Tile:
    TileTextures = {}

    def __init__(self, tile_type: TileType, obstacle: bool = False,
                 transparent: bool = True, have_sprite=False,
                 structure=None):
        self.tile_type = tile_type
        self.obstacle = obstacle
        self.transparent = transparent
        self.structure = structure
        if have_sprite:
            self.sprite = Sprite(img=Tile.TileTextures[tile_type])

    @staticmethod
    def null():
        return Tile(TileType.Empty)

    @staticmethod
    def set_textures(images: dict):
        tile_atlas = images["tiles"]
        Tile.TileTextures[TileType.Empty] = \
            tile_atlas.get_region(32 * 0, 32 * 15, 32, 32)
        Tile.TileTextures[TileType.Floor0] = \
            tile_atlas.get_region(32 * 4, 32 * 11, 32, 32)
        Tile.TileTextures[TileType.Wall0] = \
            tile_atlas.get_region(32 * 6, 32 * 4, 32, 32)
        Tile.TileTextures[TileType.Carpet0] = \
            tile_atlas.get_region(32 * 5, 32 * 11, 32, 32)
