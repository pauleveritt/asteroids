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
from typing import List

import pyglet
from pyglet import gl

from colors import Color
from drawingng import draw_ellipse_filled


class ArcadeWindow(pyglet.window.Window):
    def __init__(self, app, width: int = 400, height: int = 400):
        super().__init__(width, height)
        self.app = app
        rate = 1 / 80
        pyglet.clock.schedule_interval(self.animate, rate)

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        self.clear()
        self.app.on_draw()

    def animate(self, delta_time):
        self.app.animate(delta_time)


class ArcadeGame:
    def __init__(self, width: int = 400, height: int = 400):
        self._window = ArcadeWindow(self, width=width, height=height)

    def set_update_rate(self, rate: float):
        pyglet.clock.schedule_interval(self._window.animate, rate)

    @staticmethod
    def set_background_color(color: List[int]):
        gl.glClearColor(color[0] / 255, color[1] / 255, color[2] / 255, 1)

    @staticmethod
    def draw_circle_filled(center_x: float, center_y: float, radius: float,
                           color: Color):
        draw_ellipse_filled(center_x, center_y, radius, radius, color)

    @staticmethod
    def draw_text(text: str,
                  start_x: float, start_y: float,
                  color: Color,
                  font_size: float = 12,
                  width: int = 2000,
                  align="left",
                  font_name=('Calibri', 'Arial'),
                  bold: bool = False,
                  italic: bool = False,
                  anchor_x="left",
                  anchor_y="baseline",
                  rotation=0
                  ):
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)

        label = pyglet.text.Label(text,
                                  font_name=font_name,
                                  font_size=font_size,
                                  x=0, y=0,
                                  color=color,
                                  multiline=True,
                                  width=width,
                                  align=align,
                                  anchor_x=anchor_x,
                                  anchor_y=anchor_y,
                                  bold=bold,
                                  italic=italic)
        gl.glLoadIdentity()
        gl.glTranslatef(start_x, start_y, 0)
        gl.glRotatef(rotation, 0, 0, 1)

        label.draw()
