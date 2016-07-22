from registry import Registry, System, item_system


def test_registry_system():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    def update_position(update, entity_ids, positions, velocities):
        assert update == 'update'
        assert sorted(entity_ids) == [1, 2]
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

    r.execute('update')

    assert r.get(1, 'position').x == 11
    assert r.get(2, 'position').x == 25


def test_registry_system_item():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    seen_entity_ids = set()

    def update_position(update, entity_id, position, velocity):
        assert update == 'update'
        seen_entity_ids.add(entity_id)
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

    r.execute('update')

    assert r.get(1, 'position').x == 11
    assert r.get(2, 'position').x == 25
    assert seen_entity_ids == set([1, 2])


def test_registry_system_add_remove():
    r = Registry()
    r.register_component('position')
    r.register_component('velocity')

    def update(update, positions, velocities):
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


# def test_registry_explosion():
#     r = Registry()
#     r.register_component('position')
#     r.register_component('collision')
#     r.register_component('velocity')
#     r.register_component('debris')

#     def update_position(update, positions, velocities):
#         for position, velocity in zip(positions, velocities):
#             position.x += velocity.x_velocity
#             position.y += velocity.y_velocity

#     r.register_system(System(update_position, ['position', 'velocity']))

#     def update_collision(update, positions, collisions):
#         for position, collision in zip(positions, collisions):
#             # remove collision as we're handling it
#             update.remove(collision.entity_id, 'collision')
#             # debris flies in 4 directions
#             for x_velocity, y_velocity in [(0, -10), (10, 0),
#                                            (0, 10), (-10, 0)]:
#                 new_entity_id = update.create_entity_id()
#                 update.add(new_entity_id, 'debris',
#                            Debris())
#                 update.add(new_entity_id, 'position',
#                            Position(position.x, position.y))
#                 update.add(new_entity_id, 'velocity',
#                            Velocity(x_velocity, y_velocity))

#     class Position:
#         def __init__(self, x, y):
#             self.x = x
#             self.y = y

#     class Velocity:
#         def __init__(self, x_velocity, y_velocity):
#             self.x_velocity = x_velocity
#             self.y_velocity = y_velocity

#     class Collision:
#         def __init__(self, entity_id):
#             self.entity_id = entity_id

#     class Debris:
#         pass

#     p1 = Position(10)
#     p2 = Position(20)
#     p3 = Position(40)

#     r.add(1, 'position', p1)
#     r.add(2, 'position', p2)
#     r.add(3, 'position', p3)

#     v1 = Velocity(1)
#     v2 = Velocity(5)
#     v4 = Velocity(10)

#     r.add(1, 'velocity', v1)
#     r.add(2, 'velocity', v2)
#     r.add(4, 'velocity', v4)

#     assert r.get(1, 'position').x == 10
#     assert r.get(2, 'position').x == 20

#     assert r.get(1, 'velocity').speed == 1
#     assert r.get(2, 'velocity').speed == 5

#     r.execute('update')

#     assert r.get(1, 'position').x == 11
#     assert r.get(2, 'position').x == 25
