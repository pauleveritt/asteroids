from .arcade_ecs import DemoGame

game = DemoGame(title='Demo Game', x=20, y=40, height=50, width=100)


@DemoGame.processor('updater')
def log_edge(frame, position, velocity):
    if position == 'edge':
        print('Yep, hit the edge')


game.run()
