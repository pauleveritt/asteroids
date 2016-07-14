Welcome to asteroids's documentation!
=====================================

Let's imagine a Python gaming framework. There are others, so let's be
about what's different on this one:

- Aimed at simple development of fun, simple, 2d games, and teaching
  Python along the way.

- Not worried about high-end game development, with lots of power,
  complexity, and abstractions.

- Not worried about high-end performance.

- Not worried about tablets or phones.

- Not worried about 3d.

- Consider inheriting the mantle of PyGame.

- Scale up to "write reasonable 2d games" and down to "I just started
  learning Python"

Arcade covers most of those, though with some thinking remaining on the
balance in the last point. This repo is an experiment along those lines.
Namely, some thinking in the following direction:

- Achieve the simplicity-power balance by adopting the
  entity-component-system (ECS) patterns for game development.

- Use ECS to better scale down, and scale up, in development complexity

- Use a configuration-oriented system, instead of inheritance, to
  wire together the ECS.

- All as an experiment in cohabitation with Arcade.

Let's begin.

Hello World
===========



Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

