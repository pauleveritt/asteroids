import math
from pyglet import gl

from colors import Color


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

