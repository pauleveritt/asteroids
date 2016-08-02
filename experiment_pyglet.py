import pandas as pd
import numpy as np
import pyglet
import time


class World:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def make_world():
    amount = 1000
    position = pd.DataFrame({
        'x': np.random.rand(amount),
        'y': np.random.rand(amount)
    })
    velocity = pd.DataFrame({
        'x_speed': np.random.randn(amount) / 10,
        'y_speed': np.random.randn(amount) / 10
    })
    return World(position, velocity)


def update(w, dt):
    w.position['x'] += w.velocity['x_speed'] * dt
    w.position['y'] += w.velocity['y_speed'] * dt


def render(w):
    scaled = w.position * 600
    batch = pyglet.graphics.Batch()
    flattened = [item for sublist in scaled.values for item in sublist]
    batch.add(len(flattened) // 2, pyglet.gl.GL_POINTS, None,
              ('v2f', flattened))
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
