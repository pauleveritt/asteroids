import pyglet


class ArcadeWindow(pyglet.window.Window):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def on_draw(self):
        self.clear()
        self.app.on_draw()


class ArcadeGame:
    def __init__(self, app):
        self.window = ArcadeWindow(app)


class HelloWorldWindow(ArcadeGame):
    def __init__(self):
        super().__init__(self)
        self.label = pyglet.text.Label('Hello, world!')

    def on_draw(self):
        self.label.draw()


if __name__ == '__main__':
    HelloWorldWindow()
    pyglet.app.run()
