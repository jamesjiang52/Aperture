"""
Provide the Pathfinder class
"""

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
from utils import Payload
from abstract_view_observer import ViewObserver
from abstract_choreographer import Choreographer


@qualify
class Pathfinder:
    """
    Abstract class to calculate paths and notify Choreographers
        about next ideas
    """

    # --------------------------------- PRIVATE STATIC FIELDS --------------------------------- #

    # --------------------------------- PUBLIC STATIC FIELDS ---------------------------------- #

    PAUSE_GRANTED = 11
    PAUSE_DENIED = 12
    MAP_INFO = 13

    # --------------------------------- CONSTRUCTOR ------------------------------------------- #

    @public
    def __init__(self, conn_to_view_observer, conn_to_choreographer):
        """
        Initialize a Pathfinder with the given connections to a
            ViewObserver object and a Choreographer object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_choreographer: multiprocessing.Connection
        """
        self.__conn_to_view_observer = conn_to_view_observer
        self.__conn_to_choreographer = conn_to_choreographer

        self.__choreographer_has_idea = True
        self.__current_idea = None

        self.__require_map_update = False
        self.__pause_requested = False
        self.__choreographer_is_paused = False
        self.__map_info_requested = False
        self.__current_map = None

    # --------------------------------- MAIN EVENT LOOP --------------------------------------- #

    @public
    @final
    def main(self):
        """
        Main entry point
        :return: None
        """
        while True:
            self.run_pathfinder_iteration()

            while self.__conn_to_choreographer.poll():
                payload = self.__conn_to_choreographer.recv()
                {
                    Pathfinder.PAUSE_GRANTED: self.handle_pause_granted,
                    Pathfinder.PAUSE_DENIED: self.handle_pause_denied
                }[payload.code](payload)

            while self.__conn_to_view_observer.poll():
                payload = self.__conn_to_view_observer.recv()
                {
                    Pathfinder.MAP_INFO: self.handle_map_info
                }[payload.code](payload)

            if not self.__choreographer_has_idea:
                self.notify_idea()

            if self.__require_map_update:
                if self.__choreographer_is_paused:
                    self.request_map_info()
                else:
                    self.request_pause()

    # --------------------------------- HELPER FUNCTIONS -------------------------------------- #

    @private
    @final
    def handle_pause_granted(self, payload):
        """
        Handle the PAUSE_GRANTED message
        :param payload: Payload
        :return: None
        """
        if not self.__choreographer_is_paused:
            self.__choreographer_is_paused = True
            self.__conn_to_view_observer.send(Payload(ViewObserver.MAP_INFO_REQUEST))

    @private
    @final
    def handle_pause_denied(self, payload):
        """
        Handle the PAUSE_DENIED message
        :param payload: Payload
        :return: None
        """
        if self.__pause_requested:
            self.__pause_requested = False

    @private
    @final
    def handle_map_info(self, payload):
        """
        Handle the MAP_INFO message
        :param payload: Payload
        :return: None
        """
        if self.__require_map_update:
            self.__current_map = payload.data
            self.__require_map_update = False
            self.__map_info_requested = False
            self.allow_resume()

    @private
    @final
    def request_pause(self):
        """
        Request the Choreographer to pause so that chamber information
            can be retrieved from the ViewObserver without losing any
            frames
        :return: None
        """
        if not self.__pause_requested:
            self.__conn_to_choreographer.send(Payload(Choreographer.PAUSE_REQUEST))
            self.__pause_requested = True

    @private
    @final
    def allow_resume(self):
        """
        Allow the Choreographer to resume after a pause
        :return: None
        """
        if self.__choreographer_is_paused:
            self.__conn_to_choreographer.send(Payload(Choreographer.RESUME))
            self.__choreographer_is_paused = False
            self.__pause_requested = False

    @private
    @final
    def notify_idea(self):
        """
        Notify the Choreographer of a new idea
        :return: None
        """
        if not self.__choreographer_has_idea:
            self.__conn_to_choreographer.send(Payload(Choreographer.NEW_IDEA, self.__current_idea))
            self.__choreographer_has_idea = True

    @private
    @final
    def request_map_info(self):
        """
        Request map info from the ViewObserver
        :return: None
        """
        if not self.__map_info_requested:
            self.__conn_to_view_observer.send(Payload(ViewObserver.MAP_INFO_REQUEST))
            self.__map_info_requested = True

    # --------------------------------- PROPERTIES -------------------------------------------- #

    @property
    @protected
    def idea(self):
        """
        Get the current idea
        """
        return self.__current_idea

    @idea.setter
    @protected
    def idea(self, idea):
        """
        Setter for idea
        """
        self.__current_idea = idea
        self.__choreographer_has_idea = False

    @property
    @protected
    def update_map(self):
        """
        Get if map requires update
        """
        return self.__require_map_update

    @update_map.setter
    @protected
    def update_map(self, value):
        """
        Setter for update_map
        """
        if value:
            self.__require_map_update = value

    @property
    @protected
    def map(self):
        """
        Get the current map
        """
        return self.__current_map

    # --------------------------------- ABSTRACT METHODS -------------------------------------- #

    @protected
    def run_pathfinder_iteration(self):
        """
        Must be implemented by a subclass to run an iteration of its pathfinding
            algorithm. The main event loop will call this method on every iteration.
            This method should set the idea field if a new idea is found or set
            the update_map field if more map information is needed.
        :return: None
        """
        raise NotImplementedError("run_pathfinder_iteration method must be implemented")
