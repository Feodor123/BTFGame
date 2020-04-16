import pyglet
from pyglet.window import key
from field_entities import Door
from player import Player, PlayerController
from game import World
from tile import Tile
from fireball import Fireball
game_window = pyglet.window.Window(800, 600)

pyglet.resource.path = ['Textures']
pyglet.resource.reindex()

keys = key.KeyStateHandler()
game_window.push_handlers(keys)
Player.set_textures(pyglet.resource.image("players.png"))
Tile.set_textures({"tiles": pyglet.resource.image("tiles.png")})
Door.set_textures(pyglet.resource.image("doors.png"))
Fireball.set_textures(pyglet.resource.image("fireballs.png"))
world = World(PlayerController(keys), game_window)

info_label = pyglet.text.Label(text="", x=10, y=580)


@game_window.event
def on_draw():
    game_window.clear()
    world.draw()
    if __debug__:
        info_label.text="x: {}, y: {}, fps: {}".format(world.focus_entity.pos.x, world.focus_entity.pos.y,
                                                       pyglet.clock.get_fps())
        info_label.draw()


pyglet.clock.schedule_interval(world.update, 1 / 120.0)


if __name__ == '__main__':
    pyglet.app.run()
