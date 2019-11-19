"""
Provide the Choreographer class
"""

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
from utils import Payload
from abstract_view_observer import ViewObserver
from abstract_pathfinder import Pathfinder


@qualify
class Choreographer:
    """
    Abstract class to carry out ideas sent by Pathfinder objects by
        making decisions on what action to take based on current map
        observations
    """

    # --------------------------------- PRIVATE STATIC FIELDS --------------------------------- #

    # --------------------------------- PUBLIC STATIC FIELDS ---------------------------------- #

    PAUSE_REQUEST = 1
    RESUME = 2
    NEW_IDEA = 3
    PLAYER_INFO = 4

    # --------------------------------- CONSTRUCTOR ------------------------------------------- #

    @public
    def __init__(self, conn_to_view_observer, conn_to_pathfinder):
        """
        Initialize a Choreographer with the given connections to a
            ViewObserver object and a Pathfinder object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_pathfinder: multiprocessing.Connection
        """
        self.__conn_to_view_observer = conn_to_view_observer
        self.__conn_to_pathfinder = conn_to_pathfinder

    # --------------------------------- MAIN EVENT LOOP ---------------------------------------- #

    @public
    @final
    def main(self):
        """
        Main entry point
        :return: None
        """

    # --------------------------------- HELPER FUNCTIONS -------------------------------------- #

    @private
    @final
    def handle_pause_request(self, payload):
        """
        Handle the PAUSE_REQUEST message
        :param payload: Payload
        :return: None
        """
        if self.prepare_pause():
            self.__conn_to_pathfinder.send(Payload(Pathfinder.PAUSE_GRANTED))

    @private
    @final
    def handle_resume(self, payload):
        """
        Handle the RESUME message
        :param payload: Payload
        :return: None
        """
        self.resume()

    @private
    @final
    def handle_new_idea(self, payload):
        """
        Handle the NEW_IDEA message
        :param payload: Payload
        :return: None
        """
        pass

    @private
    @final
    def handle_player_info(self, payload):
        """
        Handle the PLAYER_INFO message
        :param payload: Payload
        :return: None
        """
        pass

    @private
    @final
    def request_player_info(self):
        """
        Request player info from the ViewObserver
        :return: None
        """
        self.__conn_to_view_observer.send(Payload(ViewObserver.PLAYER_INFO_REQUEST))

    # --------------------------------- PROPERTIES -------------------------------------------- #

    # --------------------------------- ABSTRACT METHODS -------------------------------------- #

    @protected
    def prepare_pause(self):
        """
        TODO
        :return: boolean (if pause is granted), must stop all actions
        """
        raise NotImplementedError("prepare_pause method must be implemented")

    @protected
    def resume(self):
        """
        TODO
        :return:
        """
        raise NotImplementedError("resume method must be implemented")

    @protected
    def new_idea_provided(self, idea):
        """
        Must be implemented by a subclass to handle notification events
        :param idea: Idea
        :return: None
        """
        raise NotImplementedError("notify_idea method must be implemented")
