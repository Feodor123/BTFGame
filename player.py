from entity import Entity
from animation import CreatureAnimator
from geometry import Vector, Direction, Rectangle
from enum import Enum
from pyglet.window import key
from drawing import Drawer
import pyglet


class Player(Entity):
    Basic_size = Vector(0.6, 0.6)
    Basic_max_hp = 100
    Basic_speed = 4
    Animation_frequency = 0.3

    def __init__(self, pos, controller, direction=Direction.DOWN):
        super().__init__()
        self.pos = pos
        self.max_hp = Player.Basic_max_hp
        self.hp = self.max_hp
        self.size = Player.Basic_size
        self.controller = controller
        self.direction = direction
        self.speed = Player.Basic_speed
        self.animator = CreatureAnimator({p[0]: [p[1][1], p[1][0], p[1][1], p[1][2]] for p in Player.textures.items()},
                                         Player.Animation_frequency)
        self.sprite = pyglet.sprite.Sprite(self.animator.get_texture())

    def update(self, dt, t, world):
        direction, actions = self.controller.get_behavior()
        self.animator.update(t, direction)
        if not direction.zero():
            dp = (direction/abs(direction))*self.speed*dt
            if not world.collide(self.hitbox() + dp):
                self.pos += dp

    def hitbox(self):
        return Rectangle(self.pos - self.size/2, self.size)

    def get_sprites(self):
        return [(self.sprite, 2)]

    def update_sprites(self, drawing_method):
        drawing_method(self.sprite, self.animator.get_texture(), self.pos)

    @staticmethod
    def set_textures(image):
        imgs = pyglet.image.ImageGrid(image.get_region(x=32*6, y=32*4, width=32*3, height=32*4), 4, 3)
        for i in imgs:
            i.anchor_x = i.width // 2
            i.anchor_y = i.height // 2
        Player.textures = {
            Direction.UP: imgs[0:3],
            Direction.RIGHT: imgs[3:6],
            Direction.LEFT: imgs[6:9],
            Direction.DOWN: imgs[9:12],
        }


class PlayerController:
    def __init__(self, key_handler):
        self.key_handler = key_handler

    def get_behavior(self):
        direction = Vector(0, 0)
        if self.key_handler[key.UP]:
            direction += Vector(0, 1)
        if self.key_handler[key.DOWN]:
            direction += Vector(0, -1)
        if self.key_handler[key.RIGHT]:
            direction += Vector(1, 0)
        if self.key_handler[key.LEFT]:
            direction += Vector(-1, 0)
        actions = 0
        if self.key_handler[key.SPACE]:
            actions |= ActionType.Attack
        if self.key_handler[key.ENTER]:
            actions |= ActionType.Interact
        return direction, actions


class ActionType(Enum):
    Attack = 1
    Interact = 2
