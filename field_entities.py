from entity import Entity, IObstacle, IActivable
from geometry import Vector, Direction, Rectangle
import pyglet


class Door(Entity, IObstacle, IActivable):
    Basic_size = Rectangle(0, 0, 1, 1)
    Action_area = Rectangle(0, 0, 1, 1)
    Update_frequency = 0.1

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.size = Door.Basic_size
        self.state = 0
        self.sprite = pyglet.sprite.Sprite(Door.textures[self.state])
        self.last_update = 0
        self.opened = False

    def update(self, dt, t, world):
        if self.opened and self.state < 3 and \
                self.last_update + Door.Update_frequency < t:
            self.state += 1
            self.last_update = t

    def hit(self, damage):
        pass

    def on_zero_hp(self):
        pass

    def get_sprites(self):
        return [(self.sprite, 1)]

    def update_sprites(self, drawing_method):
        drawing_method(self.sprite, Door.textures[self.state], self.pos)

    def get_size(self):
        return self.size + self.pos if self.state != 3 else Rectangle(0, 0,
                                                                      0, 0)

    def on_action(self, entity):
        self.opened = True

    def get_activate_area(self):
        return Door.Action_area + self.pos

    @staticmethod
    def set_textures(image):
        imgs = pyglet.image.ImageGrid(image.get_region(x=32 * 6, y=32 * 4,
                                                       width=32 * 1,
                                                       height=32 * 4), 4, 1)
        Door.textures = imgs[::-1]
