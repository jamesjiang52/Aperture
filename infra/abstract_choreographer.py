"""
Provide the Choreographer class
"""

from utils import Payload
from abstract_view_observer import ViewObserver
from abstract_pathfinder import Pathfinder


class Choreographer:
    """
    Abstract class to carry out ideas sent by Pathfinder objects by
        making decisions on what action to take based on current map
        observations
    """

    PAUSE_REQUEST = 1
    RESUME = 2
    NEW_IDEA = 3
    PLAYER_INFO = 4

    def __init__(self, conn_to_view_observer, conn_to_pathfinder):
        """
        Initialize a Choreographer with the given connections to a
            ViewObserver object and a Pathfinder object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_pathfinder: multiprocessing.Connection
        """
        self.__conn_to_view_observer = conn_to_view_observer
        self.__conn_to_pathfinder = conn_to_pathfinder

    def main(self):
        """
        Main entry point
        TODO: change this based on what james decides to do
        :return: None
        """

    def request_player_info(self):
        self.__conn_to_view_observer.send(Payload(ViewObserver.PLAYER_INFO_REQUEST))

    def __handle_pause_request(self):
        if self.prepare_pause():
            self.__conn_to_pathfinder.send(Payload(Pathfinder.PAUSE_GRANTED))

    def __handle_resume(self):
        self.resume()

    def prepare_pause(self):
        """
        TODO
        :return: boolean (if pause is granted), must stop all actions
        """

    def resume(self):
        """
        TODO
        :return:
        """

    def new_idea_provided(self, idea):
        """
        Must be implemented by a subclass to handle notification events
        :param idea: Idea
        :return: None
        """
        raise NotImplementedError("notify_idea method must be implemented")

    def is_running(self):
        """
        Must return True if this object is currently sending and
            receiving input and output from the game, and False
            otherwise
        :return: boolean
        """
        raise NotImplementedError("is_running method must be implemented")

    def request_pause(self):
        """

        :return: None
        """
        raise NotImplementedError("request_pause method must be implemented")

    def resume(self):
        """

        :return: None
        """
        raise NotImplementedError("resume method must be implemented")
