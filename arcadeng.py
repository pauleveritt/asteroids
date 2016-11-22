"""
A try at a different model for arcade's Window class

- Get rid of global window variable

- Allow arcade to mediate between pyglet and a game

    * Better API e.g. keypress

    * Simplifications

    * PEP 484 typing

    * Sensible defaults

- Eliminate start_render()

- Use ABC's to better indicate what *must* be filled in

- Switch to pyglet batches to improve performance

"""
from typing import List, Tuple, Union

import math
import pyglet
from pyglet import gl

RGB = Union[Tuple[int, int, int], List[int]]
RGBA = Union[Tuple[int, int, int, int], List[int]]
Color = Union[RGB, RGBA]
BLUE_GREEN: Tuple[int] = (13, 152, 186)
GREEN: Tuple[int] = (0, 255, 0)


def draw_ellipse_filled(center_x: float, center_y: float,
                        width: float, height: float, color: Color,
                        tilt_angle: float = 0):
    num_segments = 128

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    gl.glLoadIdentity()
    gl.glTranslatef(center_x, center_y, 0)
    gl.glRotatef(tilt_angle, 0, 0, 1)

    # Set color
    if len(color) == 4:
        gl.glColor4ub(color[0], color[1], color[2], color[3])
    elif len(color) == 3:
        gl.glColor4ub(color[0], color[1], color[2], 255)

    gl.glBegin(gl.GL_TRIANGLE_FAN)

    gl.glVertex3f(0, 0, 0.5)

    for segment in range(num_segments + 1):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = width * math.cos(theta)
        y = height * math.sin(theta)

        gl.glVertex3f(x, y, 0.5)

    gl.glEnd()
    gl.glLoadIdentity()


class ArcadeWindow(pyglet.window.Window):
    def __init__(self, app, width: int = 400, height: int = 400):
        super().__init__(width, height)
        self.app = app

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        self.clear()
        self.app.on_draw()


class ArcadeGame:
    def __init__(self, width: int = 400, height: int = 400):
        self.window = ArcadeWindow(self, width=width, height=height)

    @staticmethod
    def set_background_color(color: List[int]):
        gl.glClearColor(color[0] / 255, color[1] / 255, color[2] / 255, 1)

    @staticmethod
    def draw_circle_filled(center_x: float, center_y: float, radius: float,
                           color: Color):
        draw_ellipse_filled(center_x, center_y, radius, radius, color)
