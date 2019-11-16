"""
Utility functions and classes for the backend
"""

from collections import namedtuple
from enum import Enum
from typing import List


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


Checkpoint = namedtuple('Checkpoint', ['position', 'orientation', 'action'])
Checkpoint.__doc__ = """
                     Data class that represents a point of interest in a solution
                         to a chamber.
                     :param position: 3D numpy array
                     :param orientation: 3D numpy array
                     :param action: Action where is_one_shot returns True 
                         (to be executed after player reaches the desired
                         position and orientation)
                     """

Idea = List[Checkpoint]
Idea.__doc__ = """
               Represents a series of Checkpoints in the order they are to be
                   carried out
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
