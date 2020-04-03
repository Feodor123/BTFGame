from enum import Enum


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

    def __truediv__(self, num):
        return Vector(self.x / num, self.y / num)

    def __floordiv__(self, num):
        return Vector(self.x // num, self.y // num)

    def __mul__(self, num):
        return Vector(self.x * num, self.y * num)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def zero(self):
        return self.x == 0 and self.y == 0

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




class Rectangle:
    def __init__(self, *args):
        if len(args) == 2:
            self.position = args[0]
            self.size = args[1]
        elif len(args) == 4:
            self.position = Vector(args[0], args[1])
            self.size = Vector(args[2], args[3])

    def __add__(self, dv):
        return Rectangle(self.position + dv, self.size)

    def __sub__(self, dv):
        return Rectangle(self.position - dv, self.size)


class Direction(Enum):
    NONE = Vector(0, 0)
    UP = Vector(0, 1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, -1)
    LEFT = Vector(-1, 0)
