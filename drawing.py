from geometry import Vector


class Drawer:
    def __init__(self, unit_size: Vector, focus_pos: Vector, screen_center_offset: Vector):
        self.unit_size = unit_size
        self.focus_pos = focus_pos
        self.screen_center_offset = screen_center_offset
        self.final_offset = self.screen_center_offset - self.focus_pos * self.unit_size

    def draw_texture(self, sprite, texture, pos, size_in_units=Vector(1, 1), rotation=0):
        screen_pos = self.final_offset + pos  * self.unit_size
        scale = size_in_units * (self.unit_size / Vector(texture.width, texture.height))
        sprite.image = texture
        sprite.update(x=screen_pos.x, y=screen_pos.y, rotation=rotation, scale_x=scale.x, scale_y=scale.y)

    def get_tile_drawer(self, scale):
        def draw_tile(sprite, pos):
            """bit simpler - bit faster"""
            screen_pos = self.final_offset + pos * self.unit_size
            sprite.update(x=screen_pos.x, y=screen_pos.y, scale=scale)
        return draw_tile
