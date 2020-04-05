from enum import Enum
from random import randint


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)

    def __truediv__(self, obj):
        if isinstance(obj, Vector):
            return Vector(self.x / obj.x, self.y / obj.y)
        else:
            return Vector(self.x / obj, self.y / obj)

    def __floordiv__(self, obj):
        if isinstance(obj, Vector):
            return Vector(self.x // obj.x, self.y // obj.y)
        else:
            return Vector(self.x // obj, self.y // obj)

    def __mul__(self, obj):
        if isinstance(obj, Vector):
            return Vector(self.x * obj.x, self.y * obj.y)
        else:
            return Vector(self.x * obj, self.y * obj)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def zero(self):
        return self.x == 0 and self.y == 0

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_matching_directions(self):
        dirs = []
        if self.x - self.y >= 0:
            if self.x + self.y >= 0:
                dirs.append(Direction.RIGHT)
            if self.x + self.y <= 0:
                dirs.append(Direction.DOWN)
        if self.x - self.y <= 0:
            if self.x + self.y >= 0:
                dirs.append(Direction.UP)
            if self.x + self.y <= 0:
                dirs.append(Direction.LEFT)
        return dirs

    @staticmethod
    def round():
        return {Vector(1, 1), Vector(1, 0), Vector(1, -1), Vector(0, 1),
                Vector(-1, 1), Vector(-1, 0), Vector(-1, -1), Vector(0, -1)}

    @staticmethod
    def sides():
        return {Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)}


class Rectangle:
    def __init__(self, *args):
        if len(args) == 2:
            self.pos = args[0]
            self.size = args[1]
        elif len(args) == 4:
            self.pos = Vector(args[0], args[1])
            self.size = Vector(args[2], args[3])

    def __add__(self, dv):
        return Rectangle(self.pos + dv, self.size)

    def __sub__(self, dv):
        return Rectangle(self.pos - dv, self.size)

    def x1(self):
        return self.pos.x

    def y1(self):
        return self.pos.y

    def x2(self):
        return self.pos.x + self.size.x

    def y2(self):
        return self.pos.y + self.size.y

    def intersect(self, other):
        """strictly"""
        return not (other.pos.x + other.size.x <= self.pos.x or other.pos.x >= self.pos.x + self.size.x) and \
               not (other.pos.y + other.size.y <= self.pos.y or other.pos.y >= self.pos.y + self.size.y)

    def distance(self, other):
        """0 if intersect"""
        return max(self.pos.x - other.pos.x - other.size.x, other.pos.x - self.pos.x - self.size.x,
                   self.pos.y - other.pos.y - other.size.y, other.pos.y - self.pos.y - self.size.y, 0)

    @staticmethod
    def get_random(min_size, max_size, border):
        w, h = randint(min_size.x, max_size.x), randint(min_size.y, max_size.y)
        return Rectangle(randint(border.pos.x, border.pos.x + border.size.x - w),
                         randint(border.pos.y, border.pos.y + border.size.y - h), w, h)


class Direction(Enum):
    NONE = Vector(0, 0)
    UP = Vector(0, 1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, -1)
    LEFT = Vector(-1, 0)
