import pyglet

from arcadeng import ArcadeGame, BLUE_GREEN, GREEN, BLACK

SCREEN_WIDTH = 700
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
        self.draw_circle_filled(self.ball_x_position, SCREEN_HEIGHT // 2,
                                BALL_RADIUS, GREEN)
        self.draw_text("This is a simple template to start your game.",
                       10, SCREEN_HEIGHT // 2, BLACK, 20)


if __name__ == '__main__':
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    pyglet.app.run()
