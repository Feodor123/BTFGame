from entity import Entity
from geometry import Vector, Rectangle
from animation import CyclicAnimator
import pyglet

class Fireball(Entity):
    Basic_size = Rectangle(-0.2, -0.2, 0.4, 0.4)
    Update_frequency = 0.1
    Texture_size = Vector(1.5, 1.5)
    Speed = 10

    def __init__(self, pos, direction):
        super().__init__()
        self.pos = pos
        self.direction = direction
        self.size = Fireball.Basic_size
        self.animator = CyclicAnimator(Fireball.textures, Fireball.Update_frequency, direction)
        t, a = self.animator.get_texture()
        self.sprite = pyglet.sprite.Sprite(t)
        self.sprite.rotation = a

    def hitbox(self):
        return self.size + self.pos

    def update(self, dt, t, world):
        self.pos += self.direction.value * Fireball.Speed * dt
        if world.collide(self.hitbox()):
            world.remove_entity(self)
        self.animator.update(t)

    def hit(self, damage):
        pass

    def on_zero_hp(self):
        pass

    def get_sprites(self):
        return [(self.sprite, 1)]

    def update_sprites(self, drawing_method):
        t, a = self.animator.get_texture()
        drawing_method(self.sprite, t, self.pos, Fireball.Texture_size, rotation=a)

    @staticmethod
    def set_textures(image):
        imgs = pyglet.image.ImageGrid(image.get_region(x=0, y=0, width=75 * 4, height=75 * 1), 1, 4)
        for i in imgs:
            i.anchor_x = i.width // 2
            i.anchor_y = i.height // 2
        Fireball.textures = imgs[::-1]