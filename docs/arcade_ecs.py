class Game:
    def __init__(self, title: str = 'Hello World',
                 x: int = 0, y: int = 0,
                 height: int = 100, width: int = 200):
        self.title = title
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def run(self):
        pass


class DemoGame(Game):
    pass
