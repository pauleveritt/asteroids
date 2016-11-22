import pyglet

from arcadeng import ArcadeGame, BLUE_GREEN

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
BALL_RADIUS = 20


class MyGame(ArcadeGame):
    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.set_background_color(BLUE_GREEN)
        self.label = pyglet.text.Label('Hello, world!')
        self.ball_x_position = BALL_RADIUS
        self.ball_x_pixels_per_second = 70

    def on_draw(self):
        self.label.draw()


if __name__ == '__main__':
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    pyglet.app.run()
