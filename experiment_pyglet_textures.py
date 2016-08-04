import pandas as pd
import numpy as np
import pyglet
import time
from pyglet.gl import *


class World:
    def __init__(self, position, velocity, color, texture):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.texture = texture


def make_world():
    amount = 20
    position = pd.DataFrame({
        'x': np.random.rand(amount),
        'y': np.random.rand(amount)
    })
    velocity = pd.DataFrame({
        'x_speed': np.random.randn(amount) / 10,
        'y_speed': np.random.randn(amount) / 10
    })
    color = [255, 255, 255, 255] * amount
    texture = gold_image.texture.tex_coords * amount
    return World(position, velocity, color, texture)


def update(w, dt):
    w.position['x'] += w.velocity['x_speed'] * dt
    w.position['y'] += w.velocity['y_speed'] * dt


gold_image = pyglet.image.load('gold.png')
gold_image.anchor_x = gold_image.width // 2
gold_image.anchor_y = gold_image.height // 2


class TextureEnableGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)

texture_enable_group = TextureEnableGroup()


class CustomGroup(pyglet.graphics.Group):
    def __init__(self, texture):
        super().__init__(parent=texture_enable_group)
        self.texture = texture
        assert texture.target == GL_TEXTURE_2D

    def set_state(self):
        glBindTexture(self.texture.target, self.texture.id)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.texture.id == other.texture.id and
                self.texture.target == other.texture.target and
                self.parent == other.parent)

    def __hash__(self):
        return hash((self.texture.id, self.texture.target))


def render(w):
    scaled = w.position * 600
    x1 = scaled['x'] - gold_image.anchor_x
    y1 = scaled['y'] - gold_image.anchor_y
    x2 = x1 + gold_image.width
    y2 = y1 + gold_image.height
    df = pd.DataFrame({'a_x': x1, 'a_y': y1,
                       'b_x': x2, 'b_y': y1,
                       'c_x': x2, 'c_y': y2,
                       'd_x': x1, 'd_y': y2},
                      columns=['a_x', 'a_y', 'b_x', 'b_y',
                               'c_x', 'c_y', 'd_x', 'd_y'])
    r = df.values.flatten()

    batch = pyglet.graphics.Batch()
    texture = gold_image.get_texture()
    group = pyglet.sprite.SpriteGroup(texture, GL_SRC_ALPHA,
                                      GL_ONE_MINUS_SRC_ALPHA)
    batch.add(len(scaled.values) * 4, GL_QUADS, group,
              ('v2f/dynamic', r),
              ('c4B', w.color * 4),
              ('t3f', w.texture))
    batch.draw()


class Window(pyglet.window.Window):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.w = make_world()
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()
        render(self.w)
        self.fps_display.draw()

    def animate(self, delta_time):
        update(self.w, delta_time)


def main():
    window = Window()
    pyglet.clock.schedule(window.animate)
    pyglet.app.run()


if __name__ == '__main__':
    main()
