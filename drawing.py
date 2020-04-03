from pyglet.sprite import Sprite


class Drawer:
    @staticmethod
    def update_sprite(sprite: Sprite, new_texture, obj_pos, scale, offset):
        sprite.image = new_texture
        sprite.scale = scale
        v = obj_pos * scale + offset
        sprite.x = v.x
        sprite.y = v.y
