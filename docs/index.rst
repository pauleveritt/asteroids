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

Using an ECS sounds daunting. What if we could do this:

.. literalinclude:: game01.py

Some points:

- At this point we're not writing a game. We're way before that.
  Instead, we're trying to give a quick win to people that might
  never have seen Python.

- In our ECS approach, you wire stuff (components) into existing
  stuff. Thus, *we provide the "game"* and you add stuff to it.

- Which also means, we can hand you an already-working starting
  point.

- The ``run`` wires up: Arcade stuff, Pyglet stuff, and configuration
  stuff (maybe ``dectate.commit()``)

Different Window
================

Let's not under-estimate the success we just had. A bouncing ball
on the screen, maybe with some sound effects, that changes direction
when you press the space bar? Cool.

Maybe we want to tinker, but *just a little*:

.. literalinclude:: game02.py

Here we change some things about the pyglet window. We reserve the
pyglet window configuration to be done in the game constructor, but
maybe we decide to make it part of configuration, as shown later.

Change Message
==============

That's a little bit of fun. We changed something, and we could see
it pretty obviously. But it still doesn't feel like we changed the
game. Let's change the text message that ``DemoGame`` shows:

.. literalinclude:: game03.py

- Does this go as a property assignment on DemoGame instance ``game``?

- Or a method on DemoGame?

- Or change DemoGame to have some component that is in charge of
  the message?

Extend Animation
================

Our ``DemoGame`` has an animation function, and it works fine. We'd
like to slightly extend it: when you hit the edge, print something
to the console:

.. literalinclude:: game04.py

- Hmm, this got interesting. I'm adding a *second* function that
  executes on system update, in addition to the one that is in
  ``DemoGame``.

- In fact, perhaps "the one that is in ``DemoGame`` is a falsehood.
  Maybe there are bunches of functions that execute on update.

- All I had to write was a function. I didn't have to find a class
  to subclass, register that subclass, and find some magically-named
  method.

- I also didn't have to know much about the rest of the system. I asked
  for some stuff to get passed in. The system found that stuff and
  called my function with it. Makes testing easy, and possibly some other
  things (performance).

Questions
---------

- "Bunches of functions" brings up the perennial questions of
  overriding, ordering, etc.

- I dislike that 'updater' is in a string...it makes autocomplete
  and validation more magical. I wish it was ``.update``.

Other
=====

- Add a second ball

- Register a motion processor, or collission detecter

- Register some sprites

- Stop using DemoGame, instead, subclass and register your own game

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

