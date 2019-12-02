"""
Utility module for sending Portal 2 input
"""

import ctypes


controllerlib = None  # TODO

# We opt to let this memory leak since we don't know
#   when the game will stop running, plus the memory
#   is only 16 bits anyways
Controller = controllerlib.CreateController()

MOVE_HOLD = controllerlib.MOVE_HOLD
MOVE_TAP = controllerlib.MOVE_TAP

CAMERA_INSTANT = controllerlib.CAMERA_INSTANT
CAMERA_FAST = controllerlib.CAMERA_FAST
CAMERA_SLOW = controllerlib.CAMERA_SLOW
CAMERA_NUDGE = controllerlib.CAMERA_NUDGE


def move_camera(delta, speed=CAMERA_FAST):
    controllerlib.camera(Controller, delta[0], delta[1], speed)


def stop_camera():
    controllerlib.stop(Controller)


def move_forward(tap=False):
    controllerlib.forward(Controller, MOVE_TAP if tap else MOVE_HOLD)


def stop_move_forward():
    controllerlib.freeze(Controller)


def move_backward(tap=False):
    pass


def stop_move_backward():
    pass


def move_left(tap=False):
    pass


def stop_move_left():
    pass


def move_right(tap=False):
    pass


def stop_move_right():
    pass
