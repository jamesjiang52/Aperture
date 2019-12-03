"""
Utility module for sending Portal 2 input
"""

import os
from ctypes import *
import _ctypes

DLL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'input_controller', 'input_controller.dll')

_ctypes.LoadLibrary(DLL_PATH)
controllerlib = cdll.LoadLibrary(DLL_PATH)

MOVE_HOLD = c_int.in_dll(controllerlib, 'MOVE_HOLD')
MOVE_TAP = c_int.in_dll(controllerlib, 'MOVE_TAP')

CAMERA_INSTANT = c_int.in_dll(controllerlib, 'CAMERA_INSTANT')
CAMERA_FAST = c_int.in_dll(controllerlib, 'CAMERA_FAST')
CAMERA_SLOW = c_int.in_dll(controllerlib, 'CAMERA_SLOW')
CAMERA_NUDGE = c_int.in_dll(controllerlib, 'CAMERA_NUDGE')

controllerlib.CreateController.restype = c_void_p
controllerlib.DeleteController.argtypes = [c_void_p]
controllerlib.forward.argtypes = [c_void_p, c_int]
controllerlib.backward.argtypes = [c_void_p, c_int]
controllerlib.left.argtypes = [c_void_p, c_int]
controllerlib.right.argtypes = [c_void_p, c_int]
controllerlib.freeze.argtypes = [c_void_p]
controllerlib.jump.argtypes = [c_void_p]
controllerlib.interact.argtypes = [c_void_p]
controllerlib.blue.argtypes = [c_void_p]
controllerlib.orange.argtypes = [c_void_p]
controllerlib.camera.argtypes = [c_void_p, c_long, c_long, c_int]
controllerlib.stop.argtypes = [c_void_p]

# We opt to let this memory leak since we don't know
#   when the game will stop running, plus the leaked
#   memory is only 16 bits anyways
controller = controllerlib.CreateController()


def move_camera(delta, speed=CAMERA_FAST):
    controllerlib.camera(controller, int(delta[0]), int(delta[1]), speed)


def stop_camera():
    controllerlib.stop(controller)


def move_forward(tap=False):
    controllerlib.forward(controller, MOVE_TAP if tap else MOVE_HOLD)


def stop_move_forward():
    controllerlib.freeze(controller)


def move_backward(tap=False):
    controllerlib.backward(controller, MOVE_TAP if tap else MOVE_HOLD)


def stop_move_backward():
    controllerlib.freeze(controller)


def move_left(tap=False):
    controllerlib.left(controller, MOVE_TAP if tap else MOVE_HOLD)


def stop_move_left():
    controllerlib.freeze(controller)


def move_right(tap=False):
    controllerlib.right(controller, MOVE_TAP if tap else MOVE_HOLD)


def stop_move_right():
    controllerlib.freeze(controller)


def jump():
    controllerlib.jump(controller)


def interact():
    controllerlib.interact(controller)


def shoot_portal1():
    controllerlib.blue(controller)


def shoot_portal2():
    controllerlib.orange(controller)
