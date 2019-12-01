"""
Utility functions and classes for the backend
"""

from collections import namedtuple
from enum import Enum
from typing import List, Callable

import numpy as np

from ..game import input_controller


class Entity(Enum):
    """
    Observable items in Portal 2
    """
    Entrance = 0
    Exit = 1
    Button = 2
    Box = 3
    SmallButton = 4
    Launcher = 5

    def has_effect(self):
        """
        Returns True if the Entity can have an effect associated
            with it. This can be used by a search algorithm to
            get more information about the chamber
        :return: boolean
        """
        return {
            Entity.Entrance: False,
            Entity.Exit: False,
            Entity.Button: True,
            Entity.Box: False,
            Entity.SmallButton: True,
            Entity.Launcher: True
        }[self]


class Surface(Enum):
    """
    Surface types in Portal 2
    """
    P = 0
    NP = 1


class Direction(Enum):
    """
    Move directions
    """
    Forward = 1
    Backward = 2
    Left = 3
    Right = 4

    def input_function(self):
        """
        Return the input_controller movement function
            corresponding to the direction
        :return:
        """
        return {
            Direction.Forward: input_controller.move_forward,
            Direction.Backward: input_controller.move_backward,
            Direction.Left: input_controller.move_left,
            Direction.Right: input_controller.move_right
        }[self]


class Action(Enum):
    """
    Control action types
    """
    MoveForward = 1
    MoveBackward = 2
    MoveLeft = 3
    MoveRight = 4
    Jump = 5
    CameraUp = 6
    CameraDown = 7
    CameraLeft = 8
    CameraRight = 9
    Portal1 = 10
    Portal2 = 11
    Interact = 12

    def is_one_shot(self):
        """
        Returns True if the Action is single-use, and False if
            the Action is continuous
        :return: boolean
        """
        return {
            Action.MoveForward: False,
            Action.MoveBackward: False,
            Action.MoveLeft: False,
            Action.MoveRight: False,
            Action.Jump: True,
            Action.CameraUp: False,
            Action.CameraDown: False,
            Action.CameraLeft: False,
            Action.CameraRight: False,
            Action.Portal1: True,
            Action.Portal2: True,
            Action.Interact: True
        }[self]

    def execute(self):
        """
        Input the Action to the game if it is one-shot
        :return: None
        """
        if self == Action.Jump:
            input_controller.jump()
        elif self == Action.Portal1:
            input_controller.shoot_blue_portal()
        elif self == Action.Portal2:
            input_controller.shoot_orange_portal()
        elif self == Action.Interact:
            input_controller.interact()
        else:
            raise ValueError(f"Action {self.name} is not one-shot")


Checkpoint = namedtuple('Checkpoint', ['position', 'orientation', 'action', 'direction'], defaults=(None, None, None))
Checkpoint.__doc__ = """
                     Data class that represents a point of interest in a solution
                         to a chamber.
                     :param position: 3D numpy array
                     :param orientation: 3D numpy array
                     :param action: Action where is_one_shot returns True 
                         (to be executed after player reaches the desired
                         position and orientation)
                     :param direction: Direction (for use after/during jump
                         actions only) 
                     """

Idea = Callable[[np.ndarray], List[Checkpoint]]
Idea.__doc__ = """
               Given a position, return a series of Checkpoints in the order they
                   are to be carried out
               """

EntityObservation = namedtuple('EntityObservation', ['entity', 'position', 'orientation'])
EntityObservation.__doc__ = """
                            Data class that represents the observation of an Entity
                            :param entity: Entity
                            :param position: 3D numpy array
                            :param orientation: 3D numpy array
                            """

SurfaceObservation = namedtuple('SurfaceObservation', ['surface', 'corners', 'orientation'])
SurfaceObservation.__doc__ = """
                             Data class that represents the observation of a Surface
                             :param surface: Surface
                             :param corners: 3x4 numpy array, where the columns are the corner
                                 positions ordered by following the perimeter in either direction.
                                 The surface need not be in a rectangle, or be a maximally
                                 contiguous block
                             :param orientation: 3D numpy array
                             """

ReferenceObservation = namedtuple('ReferenceObservation', ['position', 'id'])
ReferenceObservation.__doc__ = """
                               Data class that represents the observation of a reference point
                               :param position: 3D numpy array
                               :param id: int
                               """

Payload = namedtuple('Payload', ['code', 'data'], defaults=(None,))


def normalize(arr):
    """
    Returns the given array normalized to have magnitude 1
    :param arr: 3D numpy array
    :return: 3D numpy array
    """
    norm = np.linalg.norm(arr)

    if norm == 0:
        raise ValueError("Array cannot be the zero vector")

    return arr / norm


def are_positions_close(pos1, pos2, epsilon):
    """
    Returns True if pos1 is epsilon-close to pos2, otherwise False
    :param pos1: 3D numpy array
    :param pos2: 3D numpy array
    :param epsilon: float
    :return: boolean
    """
    return np.linalg.norm(pos1 - pos2) <= epsilon


def are_orientations_close(or1, or2, epsilon):
    """
    Returns True if or1 is epsilon-close to or2, otherwise False
    :param or1: 3D numpy array
    :param or2: 3D numpy array
    :param epsilon: -1 <= float <= 1
    :return: boolean
    """
    return np.dot(normalize(or1), normalize(or2)) >= epsilon
