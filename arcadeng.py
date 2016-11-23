"""
A try at a different model for arcade's Window class

- Get rid of global window variable
- Allow arcade to mediate between pyglet and a game
    * Better API than pyglet
    * PEP 484 typing
- Eliminate start_render()

Later:
* Batching for sprites to improve performance
* ABCs
"""
from typing import List

import pyglet
from pyglet import gl

from colors import Color
from drawingng import draw_ellipse_filled, draw_text


class ArcadeWindow(pyglet.window.Window):
    def __init__(self, app, width: int = 400, height: int = 400):
        super().__init__(width, height)
        self.app = app
        rate = 1 / 800
        pyglet.clock.schedule_interval(self.animate, rate)

        # TODO: Make this on-demand
        self.fps_display = pyglet.clock.ClockDisplay()

    def animate(self, delta_time):
        self.app.update_model(delta_time)

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        if self.app.show_fps:
            self.fps_display.draw()
        self.app.on_draw()

    def on_key_press(self, key, key_modifiers):
        self.app.on_key_press(key, key_modifiers)


class ArcadeGame:
    def __init__(self, width: int = 400, height: int = 400):
        self._window = ArcadeWindow(self, width=width, height=height)
        self.show_fps: bool = True

    def set_update_rate(self, rate: float):
        pyglet.clock.schedule_interval(self._window.animate, rate)

    @property
    def window(self):
        return self._window

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
        draw_text(text=text, start_x=start_x, start_y=start_y,
                  color=color, font_size=font_size, width=width,
                  align=align, font_name=font_name, bold=bold,
                  italic=italic, anchor_x=anchor_x, anchor_y=anchor_y,
                  rotation=rotation
                  )
