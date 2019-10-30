# Aperture

## Table of contents
* [Description](#description)
* [Game setup](#game-setup)
* [License](#license)

## Description
Aperture is an AI agent designed to be able to navigate and solve test chambers in Valve's popular physics-based puzzle game [Portal 2](https://en.wikipedia.org/wiki/Portal_2). It is still very much in its infant stages; a proof-of-concept is currently being developed.

## Game setup
First, copy the file ``game/graphics.cfg`` into the ``portal2/cfg`` folder in the Portal 2 installation directory (usually located at ``C:/Program Files (x86)/Steam/steamapps/common/Portal 2``).

Additionally, set the Portal 2 launch options (which can be reached by right-clicking on Portal 2 in the Steam library, selecting ``Properties...``, and clicking on ``Set launch options`` under the ``General`` tab in the new window) to ``-w 640 -h 480``. (Optionally, the game resolution can also be changed in the video options in-game.)

The following basic test map files are currently available in the ``maps`` folder in the project root directory:
* ``test_basic_empty.bsp``
* ``test_basic_stairs.bsp``
* ``test_basic_single_wall.bsp``
* ``test_basic_double_wall.bsp``
* ``test_basic_deadly_easy.bsp``
* ``test_basic_deadly_hard.bsp``

Copy these files into the ``portal2/maps`` folder in the Portal 2 installation directory. To enter one of these maps, open the developer console in game and run the following command, replacing ``map_name`` with the appropriate map name:
```
map map_name
```

Once in the server, open the console and run
```
exec graphics.cfg
```

## License
See the `LICENSE` file in the project root directory for details.
