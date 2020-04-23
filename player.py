from entity import Entity
from fireball import Fireball
from animation import CreatureAnimator
from geometry import Vector, Direction, Rectangle
from enum import Enum
from pyglet.window import key
from drawing import Drawer
import pyglet


class Player(Entity):
    Basic_size = Rectangle(-0.3, -0.5, 0.6, 0.5)
    Action_area = Rectangle(-1, -1, 2, 2)
    Basic_max_hp = 100
    Basic_speed = 4
    Animation_frequency = 0.3
    Interact_cooldown = 0.5
    Attack_cooldown = 1

    def __init__(self, pos, controller, direction=Direction.DOWN):
        super().__init__()
        self.pos = pos
        self.max_hp = Player.Basic_max_hp
        self.hp = self.max_hp
        self.size = Player.Basic_size
        self.action_area = Player.Action_area
        self.controller = controller
        self.direction = direction
        self.speed = Player.Basic_speed
        self.animator = CreatureAnimator({p[0]: [p[1][1],
                                                 p[1][0],
                                                 p[1][1],
                                                 p[1][2]]
                                          for p in Player.textures.items()},
                                         Player.Animation_frequency)
        self.sprite = pyglet.sprite.Sprite(self.animator.get_texture())
        self.last_interact = 0
        self.last_attack = 0

    def update(self, dt, t, world):
        direction, actions = self.controller.get_behavior()
        self.animator.update(t, direction)
        self.direction = self.animator.direction
        if not direction.zero():
            dp = (direction/abs(direction))*self.speed*dt
            if not world.collide(self.hitbox() + dp):
                self.pos += dp
            elif not world.collide(self.hitbox() + Vector(dp.x, 0)):
                self.pos += Vector(dp.x, 0)
            elif not world.collide(self.hitbox() + Vector(0, dp.y)):
                self.pos += Vector(0, dp.y)
        if ActionType.Interact in actions and \
                self.last_interact + Player.Interact_cooldown < t:
            world.action(self, self.action_area + self.pos)
            self.last_interact = t
        if ActionType.Attack in actions and \
                self.last_attack + Player.Attack_cooldown < t:
            world.add_entity(Fireball(self.pos, self.direction))
            self.last_attack = t

    def hitbox(self):
        return self.size + self.pos

    def get_sprites(self):
        return [(self.sprite, 2)]

    def update_sprites(self, drawing_method):
        drawing_method(self.sprite, self.animator.get_texture(), self.pos)

    @staticmethod
    def set_textures(image):
        imgs = pyglet.image.ImageGrid(image.get_region(x=32*6,
                                                       y=32*4,
                                                       width=32*3,
                                                       height=32*4), 4, 3)
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
        if self.key_handler[key.W]:
            direction += Vector(0, 1)
        if self.key_handler[key.S]:
            direction += Vector(0, -1)
        if self.key_handler[key.D]:
            direction += Vector(1, 0)
        if self.key_handler[key.A]:
            direction += Vector(-1, 0)
        actions = set()
        if self.key_handler[key.SPACE]:
            actions.add(ActionType.Attack)
        if self.key_handler[key.ENTER]:
            actions.add(ActionType.Interact)
        return direction, actions


class ActionType(Enum):
    Attack = 1
    Interact = 2
