from player import Player
from geometry import *
import pyglet


class World:
    Layer_count = 3

    def __init__(self, controller):
        self.batch = pyglet.graphics.Batch()
        self.layers = [pyglet.graphics.OrderedGroup(i) for i in range(World.Layer_count)]
        self.entities = {}
        self.focus_entity = Player(Vector(100, 100), controller)
        self.focus_pos = self.get_focus()
        self.add_entity(self. focus_entity)
        self.time = 0
        self.scale = 1

    def collide(self, rect):
        return False

    def add_entity(self, entity):
        self.entities[entity.id] = entity
        for s, i in entity.get_sprites():
            s.batch = self.batch
            s.group = self.layers[i]

    def draw(self):
        for e in self.entities.values():
            e.draw(self.scale, self.focus_pos)
        self.batch.draw()

    def get_focus(self):
        return Vector(0, 0)

    def update(self,  dt):
        self.time += dt
        for e in self.entities.values():
            e.update(dt, self.time, self)
        self.focus_pos = self.get_focus()
        self.draw()
