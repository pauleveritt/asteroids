import pyglet

from arcadeng import ArcadeGame
from colors import BLUE_GREEN, GREEN, BLACK
from keys import MOD_SHIFT, SPACE

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
BALL_RADIUS = 20


class MyGame(ArcadeGame):
    def __init__(self, width, height, title):
        super().__init__(width=width, height=height)
        self.title = title
        self.set_background_color(BLUE_GREEN)
        self.ball_x_position = BALL_RADIUS
        self.ball_x_pixels_per_second = 70

    def on_draw(self):
        self.draw_circle_filled(self.ball_x_position, SCREEN_HEIGHT // 2,
                                BALL_RADIUS, GREEN)
        self.draw_text("This is a simple template to start your game.",
                       10, SCREEN_HEIGHT // 2, BLACK, 20)

    def animate(self, delta_time):
        # Move the ball
        self.ball_x_position += self.ball_x_pixels_per_second * delta_time

        # Did the ball hit the right side of the screen while moving right?
        if self.ball_x_position > SCREEN_WIDTH - BALL_RADIUS \
                and self.ball_x_pixels_per_second > 0:
            self.ball_x_pixels_per_second *= -1

        # Did the ball hit the left side of the screen while moving left?
        if self.ball_x_position < BALL_RADIUS \
                and self.ball_x_pixels_per_second < 0:
            self.ball_x_pixels_per_second *= -1

    def on_key_press(self, key, key_modifiers):

        # See if the user hit Shift-Space
        # (Key modifiers are in powers of two, so you can detect multiple
        # modifiers by using a bit-wise 'and'.)
        if key == SPACE and key_modifiers == MOD_SHIFT:
            print(self.title + " You pressed shift-space")

        # See if the user just hit space.
        elif key == SPACE:
            print(self.title + " You pressed the space bar.")


if __name__ == '__main__':
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'My Game')
    pyglet.app.run()
