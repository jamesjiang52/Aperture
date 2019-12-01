"""
A concrete implementation of a Choreographer
"""

from time import sleep
from multiprocessing.connection import Connection

import numpy as np

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
from ..game import input_controller
import utils
from abstract_choreographer import Choreographer


@qualify
class Choreo(Choreographer):
    """
    Implementation of a Choreographer class
    """

    __IDEA_WAIT_INTERVAL = 0.05
    __TURN_WAIT_INTERVAL = 0.03
    __MOVE_WAIT_INTERVAL = 0.03

    __SLOW_CAMERA_MIN_COSINE = 0.95
    __EQUAL_MIN_COSINE = 0.99

    __SLOW_MOVE_MAX_EPSILON = 10
    __EQUAL_MAX_EPSILON = 3

    @public
    @final
    def __init__(self, conn_to_view_observer: Connection, conn_to_pathfinder: Connection):
        super().__init__(conn_to_view_observer, conn_to_pathfinder)

        self.__current_idea = None
        self.__active_idea = []

    @staticmethod
    def __get_projected_direction(start_orientation: np.ndarray, end_orientation: np.ndarray) -> np.ndarray:
        """
        Return a 2D vector representing the direction to move the
            camera in order to rotate from the given start orientation
            to the given end orientation. Positive components represent
            the downward and rightward directions.
        :param start_orientation: 3D numpy array
        :param end_orientation: 3D numpy array
        :return: 2D numpy array
        """
        start_orientation = utils.normalize(start_orientation)
        end_orientation = utils.normalize(end_orientation)

        theta1 = np.arctan(start_orientation[1] / start_orientation[0])
        phi1 = np.arccos(start_orientation[2])
        theta2 = np.arccos(end_orientation[1] / end_orientation[0])
        phi2 = np.arccos(end_orientation[2])

        return np.array([theta1 - theta2, phi2 - phi1])

    @protected
    def wait_for_idea(self, clear: bool = False) -> None:
        """
        Do nothing until a new idea is provided, setting the
            current idea to None if clear is set
        :param clear: bool
        :return: None
        """
        if clear:
            self.__current_idea = None

        while self.idea == self.__current_idea or not self.idea:
            sleep(Choreo.__IDEA_WAIT_INTERVAL)
        else:
            self.__current_idea = self.idea
            self.__active_idea = self.__current_idea(self.player_info[0])

    @protected
    def turn(self, target_orientation: np.ndarray, exact: bool = True) -> None:
        """
        Turn the player from the current orientation to the given
            target orientation
        :param target_orientation: 3D numpy array
        :param exact: bool
        :return: None
        """
        current_orientation = self.player_info[1]
        direction = Choreo.__get_projected_direction(current_orientation, target_orientation)
        input_controller.move_camera(direction, speed=input_controller.CAMERA_FAST)

        while not utils.are_orientations_close(self.player_info[1],
                                               target_orientation,
                                               Choreo.__SLOW_CAMERA_MIN_COSINE):
            sleep(Choreo.__TURN_WAIT_INTERVAL)

        input_controller.stop_camera()

        if not exact:
            return

        last_orientation = None
        while True:
            current_orientation = self.player_info[1]
            if utils.are_orientations_close(current_orientation, target_orientation, Choreo.__EQUAL_MIN_COSINE):
                break
            if current_orientation == last_orientation:
                sleep(Choreo.__TURN_WAIT_INTERVAL)
                continue
            input_controller.move_camera(Choreo.__get_projected_direction(current_orientation, target_orientation),
                                         speed=input_controller.CAMERA_NUDGE)
            last_orientation = current_orientation

    @protected
    def go_to_checkpoint_state(self,
                               checkpoint: utils.Checkpoint,
                               position_exact: bool = True,
                               orientation_exact: bool = True) -> None:
        """
        Moves the player from the current position to the given
            position and orientation specified by the checkpoint,
            assuming that the checkpoint is walkable from the current
            position
        :param checkpoint: Checkpoint
        :param position_exact: bool
        :param orientation_exact: bool
        :return: None
        """
        current_position = self.player_info[0]
        target_position = checkpoint.position

        current_position[2] = 0
        target_position[2] = 0
        self.turn(target_position - current_position, exact=position_exact)

        input_controller.move_forward()

        while True:
            current_position = self.player_info[0]
            current_position[2] = 0
            if utils.are_positions_close(current_position, target_position, Choreo.__SLOW_MOVE_MAX_EPSILON):
                break
            sleep(Choreo.__MOVE_WAIT_INTERVAL)

        input_controller.stop_move_forward()

        if position_exact:
            last_position = None
            while True:
                current_position = self.player_info[0]
                current_position[2] = 0
                if utils.are_positions_close(current_position, target_position, Choreo.__EQUAL_MAX_EPSILON):
                    break
                if current_position == last_position:
                    sleep(Choreo.__MOVE_WAIT_INTERVAL)
                    continue
                input_controller.move_forward(tap=True)
                last_position = current_position

        self.turn(checkpoint.orientation, exact=orientation_exact)

    @protected
    def execute_idea(self) -> bool:
        """
        Carry out a single checkpoint of the current idea, returning
            True if successful and False otherwise
        :return: bool
        """
        if not self.__active_idea:
            return False

        checkpoint = self.__active_idea[0]
        self.go_to_checkpoint_state(checkpoint, position_exact=True, orientation_exact=True)

        if checkpoint.action:
            checkpoint.action.execute()
            if checkpoint.action == utils.Action.Jump and checkpoint.direction:
                # ideally, we would move in the direction until the player's z
                # position stops changing, but for now we just tap the direction
                checkpoint.direction.input_function(tap=True)

        return True

    @protected
    @final
    def run_choreography(self) -> None:
        """
        Start coordinating frames observed by the ViewObserver and
            actions to take
        :return: None
        """
        while True:
            if not self.__active_idea:
                self.wait_for_idea()

            if self.execute_idea():
                self.__active_idea = self.__active_idea[1:]
            else:
                self.wait_for_idea(clear=True)
