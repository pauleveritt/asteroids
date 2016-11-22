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
from typing import List, Tuple

import pyglet
from pyglet import gl

BLUE_GREEN: Tuple[int] = (13, 152, 186)


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
