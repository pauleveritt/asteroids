import pandas as pd
import numpy as np
import arcade
import time


class World:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


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
    return World(position, velocity)


def update(w, dt):
    w.position['x'] += w.velocity['x_speed'] * dt
    w.position['y'] += w.velocity['y_speed'] * dt


def render(w):
    scaled = w.position * 600
    e = arcade.create_ellipse(10, 10, arcade.color.RED)
    for index, row in scaled.iterrows():
        arcade.render_ellipse_filled(e, row.x, row.y)
        #arcade.draw_circle_filled(row.x, row.y, 10, arcade.color.RED)


class MyApp(arcade.Window):
    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.w = make_world()

    def on_draw(self):
        #s = time.time()
        arcade.start_render()
        render(self.w)
        #e = time.time()
        #print("Draw:", e - s)

    def animate(self, delta_time):
        #s = time.time()
        update(self.w, delta_time)
        #e = time.time()
        #print("Animate:", e - s)


def main():
    window = MyApp(600, 600)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
