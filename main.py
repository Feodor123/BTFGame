import pyglet
from pyglet.window import key
from player import Player, PlayerController
from game import World
import geometry
game_window = pyglet.window.Window(800, 600)

pyglet.resource.path = ['Textures']
pyglet.resource.reindex()

keys = key.KeyStateHandler()
game_window.push_handlers(keys)
Player.get_textures(pyglet.resource.image("players.png"))
world = World(PlayerController(keys))

gps_label = pyglet.text.Label(text="", x=10, y=580)


@game_window.event
def on_draw():
    game_window.clear()
    if __debug__:
        gps_label.text="x: {}, y: {}".format(world.focus_entity.pos.x, world.focus_entity.pos.y)
        gps_label.draw()
    world.draw()


pyglet.clock.schedule_interval(world.update, 1 / 120.0)


if __name__ == '__main__':
    pyglet.app.run()
