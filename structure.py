from tile import TileType, Tile
from geometry import Vector, Rectangle, Direction


class Room:
    """basic implementation; to be inherited"""
    def __init__(self, shape: Rectangle, floor: TileType, wall: TileType):
        self.shape = shape
        self.floor = floor
        self.wall = wall
        self.doors = []

    def fill(self, field):
        for x in range(self.shape.pos.x, self.shape.pos.x + self.shape.size.x):
            for y in range(self.shape.pos.y, self.shape.pos.y + self.shape.size.y):
                field[x, y] = Tile(self.floor, have_sprite=True, structure=self)

    def border(self, field, replace: bool = False):
        for x in range(self.shape.pos.x - 1, self.shape.pos.x + self.shape.size.x + 1):
            if replace or field[x, self.shape.pos.y - 1].tile_type == TileType.Empty:
                field[x, self.shape.pos.y - 1] = Tile(self.wall, obstacle=True, have_sprite=True, structure=self)
            if replace or field[x, self.shape.pos.y + self.shape.size.y].tile_type == TileType.Empty:
                field[x, self.shape.pos.y + self.shape.size.y] = Tile(self.wall, obstacle=True, have_sprite=True,
                                                                      structure=self)
        for y in range(self.shape.pos.y, self.shape.pos.y + self.shape.size.y):
            if replace or field[self.shape.pos.x - 1, y].tile_type == TileType.Empty:
                field[self.shape.pos.x - 1, y] = Tile(self.wall, obstacle=True, have_sprite=True, structure=self)
            if replace or field[self.shape.pos.x + self.shape.size.x, y].tile_type == TileType.Empty:
                field[self.shape.pos.x + self.shape.size.x, y] = Tile(self.wall, obstacle=True, have_sprite=True,
                                                                      structure=self)

    def get_border(self):
        borders = set()
        for x in range(self.shape.pos.x - 1, self.shape.pos.x + self.shape.size.x + 1):
            borders.add(Vector(x, self.shape.pos.y - 1))
            borders.add(Vector(x, self.shape.pos.y + self.shape.size.y))
        for y in range(self.shape.pos.y, self.shape.pos.y + self.shape.size.y):
            borders.add(Vector(self.shape.pos.x - 1, y))
            borders.add(Vector(self.shape.pos.x + self.shape.size.x, y))
        return borders

    def get_corners(self):
        return {Vector(self.shape.x1() - 1, self.shape.y1() - 1),
                Vector(self.shape.x2(), self.shape.y1() - 1),
                Vector(self.shape.x1() - 1, self.shape.y2()),
                Vector(self.shape.x2(), self.shape.y2())}

    def possible_doors(self):
        candidates = self.get_border() - self.get_corners()
        for door in self.doors:
            for d in Direction:
                candidates.discard(door + d.value)
        return candidates


class ToiletRoom(Room):
    def __init__(self, shape: Rectangle, floor: TileType, wall: TileType, carpet: TileType):
        if shape.size.x % 2 == 0 or shape.size.y % 2 == 0:
            raise AssertionError()
        self.shape = shape
        self.floor = floor
        self.wall = wall
        self.carpet = carpet
        self.doors = []

    def fill(self, field):
        super(ToiletRoom, self).fill(field)
        center = self.shape.pos + self.shape.size // 2;
        for x in range(center.x - 1,center.x + 2):
            for y in range(center.y - 1,center.y + 2):
                field[x,y] = Tile(self.carpet, have_sprite=True, structure=self)


class Road:
    def __init__(self, path: list, floor: TileType, wall: TileType):
        self.path = path
        self.floor = floor
        self.wall = wall

    def fill(self, field):
        for v in self.path:
            field[v.x, v.y] = Tile(self.floor, have_sprite=True, structure=self)

    def border(self, field, replace: bool = False):
        to_fill = set()
        for i in range(1, len(self.path) - 1):
            for v in Vector.round():
                to_fill.add(self.path[i] + v)
        for v in self.path:
            to_fill.discard(v)
        for v in to_fill:
            if replace or field[v.x, v.y].tile_type == TileType.Empty:
                field[v.x, v.y] = Tile(self.wall, obstacle=True, have_sprite=True, structure=self)