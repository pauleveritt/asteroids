import pandas as pd
import numpy as np
import pyglet
import time


class World:
    def __init__(self, position, velocity, sprites, batch):
        self.position = position
        self.velocity = velocity
        self.sprites = sprites
        self.batch = batch


def make_world():
    amount = 100
    position = pd.DataFrame({
        'x': np.random.rand(amount),
        'y': np.random.rand(amount)
    })
    velocity = pd.DataFrame({
        'x_speed': np.random.randn(amount) / 10,
        'y_speed': np.random.randn(amount) / 10
    })
    batch = pyglet.graphics.Batch()
    sprites = []
    for x, y in position.values:
        sprites.append(pyglet.sprite.Sprite(
            gold_image, x, y, batch=batch))
    return World(position, velocity, sprites, batch)


def update(w, dt):
    w.position['x'] += w.velocity['x_speed'] * dt
    w.position['y'] += w.velocity['y_speed'] * dt


gold_image = pyglet.image.load('gold.png')
gold_image.anchor_x = gold_image.width // 2
gold_image.anchor_y = gold_image.height // 2


def render(w):
    scaled = w.position * 600
    for i, (x, y) in enumerate(scaled.values):
        s = w.sprites[i]
        s.x = x
        s.y = y
    w.batch.draw()


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
