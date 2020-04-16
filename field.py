from geometry import Vector, Rectangle, Direction
from field_entities import Door
from tile import Tile, TileType
from structure import Room, ToiletRoom, Road
from collections import deque
import math
from random import randint, choice


class GameField:
    def __init__(self, game, size: Vector):
        self.size = size
        self.rooms = []
        self.roads = []
        self._tiles = [[Tile(TileType.Empty, have_sprite=True) for y in range(self.size.y)] for x in range(self.size.x)]
        self.sprites = []
        self.min_room_size = Vector(4, 4)
        self.max_room_size = Vector(8, 8)
        self.room_count = 20
        self.generate(game)

    def collide(self, rect: Rectangle):
        for x in range(math.floor(rect.pos.x), math.floor(rect.pos.x + rect.size.x) + 1):
            for y in range(math.floor(rect.pos.y), math.floor(rect.pos.y + rect.size.y) + 1):
                if self[x, y].obstacle:
                    return True
        return False

    def get_sprites(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                yield self[x, y].sprite, 0

    def update_sprites(self, tile_draw_method):
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile_draw_method(self[x, y].sprite, Vector(x, y))

    def on_field(self, v, indent=0):
        return indent <= v.x < self.size.x - indent and indent <= v.y < self.size.y - indent

    def on_floor(self, v):
        return self[v.x, v.y].tile_type != TileType.Empty

    def __getitem__(self, key):
        return self._tiles[key[0]][key[1]] if 0 <= key[0] < self.size.x and \
                                              0 <= key[1] < self.size.y else Tile.null()

    def __setitem__(self, key, item):
        if 0 <= key[0] < self.size.x and 0 <= key[1] < self.size.y:
            self._tiles[key[0]][key[1]] = item

    """**************Generation section****************"""

    def generate(self, game):
        self.generate_rooms(game)

    def generate_rooms(self, game, min_distance=1):
        border = Rectangle(Vector(1, 1), self.size - Vector(2, 2))
        for i in range(1000):
            rect = Rectangle.get_random(Vector(5, 5), Vector(5, 5), border)
            for x, y in [(x, y) for x in range(rect.pos.x - min_distance, rect.pos.x + rect.size.x + min_distance + 1)
                         for y in range(rect.pos.y - min_distance, rect.pos.y + rect.size.y + min_distance + 1)]:
                if self[x, y].tile_type != TileType.Empty and not self[x, y].obstacle:
                    break
            else:
                self.add_room(ToiletRoom(rect, TileType.Floor0, TileType.Wall0, TileType.Carpet0), 0)
                break
        for i in range(1000):
            rect = Rectangle.get_random(self.min_room_size, self.max_room_size, border)
            for x, y in [(x, y) for x in range(rect.pos.x - min_distance, rect.pos.x + rect.size.x + min_distance + 1)
                         for y in range(rect.pos.y - min_distance, rect.pos.y + rect.size.y + min_distance + 1)]:
                if self[x, y].tile_type != TileType.Empty and not self[x, y].obstacle:
                    break
            else:
                self.add_room(Room(rect, TileType.Floor0, TileType.Wall0), 2 if len(self.rooms) > 0 else 0)
                if len(self.rooms) >= self.room_count:
                    break
        for r in self.roads:
            r.border(self)
        for p in {d for r in self.rooms for d in r.doors}:
            game.add_entity(Door(p))

    def add_room(self, room, num_connects=0):
        self.rooms.append(room)
        room.fill(self)
        room.border(self)
        self.connect_room(room, num_connects)

    def connect_room(self, room, connections_count):
        possible_out_doors = room.possible_doors()
        possible_in_doors = {v for r in self.rooms if r != room for v in r.possible_doors()}
        while len(room.doors) < connections_count and len(possible_out_doors) > 0:
            door = choice(tuple(possible_out_doors))
            path = self.dfs(door, lambda v: self.on_field(v, 1) and self[v.x, v.y].tile_type == TileType.Empty,
                            lambda v: v in possible_in_doors or
                            type(self[v.x, v.y].structure) == Road and not self[v.x, v.y].obstacle)
            if path is None:
                possible_out_doors.remove(door)
                continue
            road = Road(path, TileType.Floor0, TileType.Wall0)
            self.roads.append(road)
            room.doors.append(door)
            if path[-1] in possible_in_doors:
                for r in self.rooms:
                    if r != room and path[-1] in r.possible_doors():
                        r.doors.append(path[-1])
                        break
                for dv in Vector.sides():
                    possible_in_doors.discard(path[-1] + dv)
            for dv in Vector.sides():
                possible_out_doors.discard(door + dv)
            road.fill(self)
        if connections_count != 0 and len(room.doors) == 0:
            raise AssertionError("weird...")

    @staticmethod
    def dfs(start, passable_checker, end_checker):
        from_dict = {start: None}
        queue = deque([start])
        if end_checker(start):
            return [start]
        while len(queue) > 0:
            v = queue.popleft()
            for dv in Vector.sides():
                if end_checker(v + dv):
                    answ = [v + dv]
                    while not (v is None):
                        answ.append(v)
                        v = from_dict[v]
                    answ.reverse()
                    return answ
                v2 = v + dv
                if v2 not in from_dict and passable_checker(v2):
                    from_dict[v2] = v
                    queue.append(v2)
        return None
