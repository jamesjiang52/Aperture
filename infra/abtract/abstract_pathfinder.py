"""
Provide the Pathfinder class
"""

from time import time, sleep
from threading import Thread, RLock
from multiprocessing.connection import Connection

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
from utils import Payload, Idea
from mapping_utils import Observation
from abstract_view_observer import ViewObserver
from abstract_choreographer import Choreographer


@qualify
class Pathfinder:
    """
    Abstract class to calculate paths and notify Choreographers
        about next ideas
    """

    # --------------------------------- PRIVATE STATIC FIELDS --------------------------------- #

    __ITERATION_TIME = 0.1

    # --------------------------------- PUBLIC STATIC FIELDS ---------------------------------- #

    MAP_INFO = 13

    # --------------------------------- CONSTRUCTOR ------------------------------------------- #

    @public
    def __init__(self, conn_to_view_observer: Connection, conn_to_choreographer: Connection):
        """
        Initialize a Pathfinder with the given connections to a
            ViewObserver object and a Choreographer object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_choreographer: multiprocessing.Connection
        """
        self.__conn_to_view_observer = conn_to_view_observer
        self.__conn_to_choreographer = conn_to_choreographer

        self.__pathfinder_thread = None
        self.__idea_lock = RLock()
        self.__map_lock = RLock()

        self.__choreographer_has_idea = True
        self.__current_idea = None

        self.__require_map_update = False
        self.__map_info_requested = False
        self.__current_map = None

    # --------------------------------- MAIN EVENT LOOP --------------------------------------- #

    @public
    @final
    def main(self) -> None:
        """
        Main entry point
        :return: None
        """
        self.__pathfinder_thread = Thread(target=self.run_pathfinder)
        self.__pathfinder_thread.start()

        while True:
            start = time()

            while self.__conn_to_view_observer.poll():
                payload = self.__conn_to_view_observer.recv()
                {
                    Pathfinder.MAP_INFO: self.handle_map_info
                }[payload.code](payload)

            if not self.__choreographer_has_idea:
                self.notify_idea()

            if self.__require_map_update:
                self.request_map_info()

            sleep(Pathfinder.__ITERATION_TIME - time() + start)

    # --------------------------------- HELPER FUNCTIONS -------------------------------------- #

    @private
    @final
    def handle_map_info(self, payload: Payload) -> None:
        """
        Handle the MAP_INFO message
        :param payload: Payload
        :return: None
        """
        with self.__map_lock:
            if self.__require_map_update:
                self.__current_map = payload.data
                self.__require_map_update = False
                self.__map_info_requested = False
                self.allow_resume()

    @private
    @final
    def notify_idea(self) -> None:
        """
        Notify the Choreographer of a new idea
        :return: None
        """
        with self.__idea_lock:
            if not self.__choreographer_has_idea:
                self.__conn_to_choreographer.send(
                    Payload(Choreographer.NEW_IDEA, self.__current_idea))
                self.__choreographer_has_idea = True

    @private
    @final
    def request_map_info(self) -> None:
        """
        Request map info from the ViewObserver
        :return: None
        """
        if not self.__map_info_requested:
            self.__conn_to_view_observer.send(Payload(ViewObserver.MAP_INFO_REQUEST))
            self.__map_info_requested = True

    # --------------------------------- SUBCLASS INTERFACE ------------------------------------ #

    @property
    @protected
    def idea(self) -> Idea:
        """
        Get the current idea
        """
        with self.__idea_lock:
            return self.__current_idea

    @idea.setter
    @protected
    def idea(self, idea: Idea) -> None:
        """
        Setter for idea
        """
        with self.__idea_lock:
            self.__current_idea = idea
            self.__choreographer_has_idea = False

    @property
    @protected
    def map(self) -> Observation:
        """
        Get the current map
        """
        with self.__map_lock:
            return self.__current_map

    @protected
    def require_map_update(self) -> None:
        """
        Set the map to require an update from the ViewObserver
        :return: None
        """
        with self.__map_lock:
            self.__require_map_update = True

    # --------------------------------- ABSTRACT METHODS -------------------------------------- #

    @protected
    def run_pathfinder(self) -> None:
        """
        Must be implemented by a subclass to run its pathfinding algorithm. This method
            should call self.idea to get the current idea and set the value of self.idea
            once another idea is found. This method can make use of self.map to get the
            chamber entities currently known to the ViewObserver, and can call
            self.require_map_update() at any point if the search requires more chamber
            information
        :return: None
        """
        raise NotImplementedError("run_pathfinder method must be implemented")
