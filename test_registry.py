from registry import Registry, System, item_system


def test_registry_system():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    def update_position(positions, velocities):
        for position, velocity in zip(positions, velocities):
            position.x += velocity.speed

    r.register_system(System(update_position, ['position', 'velocity']))

    class Position:
        def __init__(self, x):
            self.x = x

    class Velocity:
        def __init__(self, speed):
            self.speed = speed

    p1 = Position(10)
    p2 = Position(20)
    p3 = Position(40)

    r.add(1, 'position', p1)
    r.add(2, 'position', p2)
    r.add(3, 'position', p3)

    v1 = Velocity(1)
    v2 = Velocity(5)
    v4 = Velocity(10)

    r.add(1, 'velocity', v1)
    r.add(2, 'velocity', v2)
    r.add(4, 'velocity', v4)

    assert r.get(1, 'position').x == 10
    assert r.get(2, 'position').x == 20

    assert r.get(1, 'velocity').speed == 1
    assert r.get(2, 'velocity').speed == 5

    r.execute()

    assert r.get(1, 'position').x == 11
    assert r.get(2, 'position').x == 25


def test_registry_system_item():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    def update_position(position, velocity):
        position.x += velocity.speed

    r.register_system(item_system(update_position, ['position', 'velocity']))

    class Position:
        def __init__(self, x):
            self.x = x

    class Velocity:
        def __init__(self, speed):
            self.speed = speed

    p1 = Position(10)
    p2 = Position(20)
    p3 = Position(40)

    r.add(1, 'position', p1)
    r.add(2, 'position', p2)
    r.add(3, 'position', p3)

    v1 = Velocity(1)
    v2 = Velocity(5)
    v4 = Velocity(10)

    r.add(1, 'velocity', v1)
    r.add(2, 'velocity', v2)
    r.add(4, 'velocity', v4)

    assert r.get(1, 'position').x == 10
    assert r.get(2, 'position').x == 20

    assert r.get(1, 'velocity').speed == 1
    assert r.get(2, 'velocity').speed == 5

    r.execute()

    assert r.get(1, 'position').x == 11
    assert r.get(2, 'position').x == 25


def test_registry_system_add_remove():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    def update(positions, velocities):
        pass

    s = System(update, ['position', 'velocity'])

    r.register_system(s)

    class Position:
        def __init__(self, x):
            self.x = x

    class Velocity:
        def __init__(self, speed):
            self.speed = speed

    p1 = Position(10)
    p2 = Position(20)
    p3 = Position(40)

    r.add(1, 'position', p1)
    r.add(2, 'position', p2)
    r.add(3, 'position', p3)
    assert s.entity_ids == set()

    v1 = Velocity(1)
    v2 = Velocity(5)
    v4 = Velocity(10)

    r.add(1, 'velocity', v1)
    assert s.entity_ids == set([1])
    r.add(2, 'velocity', v2)
    assert s.entity_ids == set([1, 2])
    r.add(4, 'velocity', v4)
    assert s.entity_ids == set([1, 2])

    r.remove(1, 'velocity')
    assert s.entity_ids == set([2])
