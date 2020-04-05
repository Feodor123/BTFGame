from player import Player
from field import GameField
from geometry import Vector, Rectangle
from drawing import Drawer
from random import randint
import pyglet


class World:
    Layer_count = 3

    def __init__(self, controller, game_window):
        self.game_window = game_window
        self.batch = pyglet.graphics.Batch()
        self.layers = [pyglet.graphics.OrderedGroup(i) for i in range(World.Layer_count)]
        self.entities = {}
        self.focus_entity = Player(Vector(0, 0), controller)
        self.focus_pos = self.get_focus()
        self.add_entity(self.focus_entity)
        self.time = 0
        self.scale = 1
        self.field_size = Vector(30, 30)
        self.field = GameField(self.field_size)
        self.focus_entity.pos = self.random_free(self.focus_entity.size)

        for s, i in self.field.get_sprites():
            s.batch = self.batch
            s.group = self.layers[i]

    def random_free(self, size):
        v = Vector(randint(0, self.field_size.x - 1), randint(0, self.field_size.y - 1))
        while self.collide(Rectangle(v - size/2, size)):
            v = Vector(randint(0, self.field_size.x - 1), randint(0, self.field_size.y - 1))
        return v

    def collide(self, rect: Rectangle):
        return self.field.collide(rect)

    def add_entity(self, entity):
        self.entities[entity.id] = entity
        for s, i in entity.get_sprites():
            s.batch = self.batch
            s.group = self.layers[i]

    def draw(self):
        drawer = Drawer(Vector(32, 32) * self.scale, self.get_focus(),
                        Vector(self.game_window.width / 2, self.game_window.height / 2))
        for e in self.entities.values():
            e.update_sprites(drawer.draw_texture)
        self.field.update_sprites(drawer.get_tile_drawer(self.scale))
        self.batch.draw()

    def get_focus(self):
        return self.focus_entity.pos

    def update(self,  dt):
        self.time += dt
        for e in self.entities.values():
            e.update(dt, self.time, self)
        self.focus_pos = self.get_focus()
        self.draw()
