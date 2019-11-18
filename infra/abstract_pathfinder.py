"""
Provide the Pathfinder class
"""

from threading import Thread, Event
from time import sleep

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

    iteration_time = 1.5

    PAUSE_GRANTED = 11
    MAP_INFO = 12

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

        self.__pathfinder_pause_requested = Event()
        self.__current_idea = None
        self.__idea_changed = False
        self.__choreographer_has_idea = True

    @public
    @final
    def main(self):
        """
        Main entry point
        :return: None
        """
        while True:
            thread = Thread(target=self.resume_pathfinder)
            thread.start()
            sleep(Pathfinder.iteration_time)
            self.__pathfinder_pause_requested.set()
            thread.join()
            if self.__idea_changed:
                pass
            else:
                pass

    @private
    @final
    def request_pause(self):
        """
        Request the Choreographer to pause so that chamber information
            can be retrieved from the ViewObserver without losing any
            frames
        :return: None
        """
        self.__conn_to_choreographer.send(Payload(Choreographer.PAUSE_REQUEST))

    @private
    @final
    def allow_resume(self):
        """
        Allow the Choreographer to resume after a pause
        :return: None
        """
        self.__conn_to_choreographer.send(Payload(Choreographer.RESUME))

    @private
    @final
    def handle_pause_granted(self):
        """
        Handle the PAUSE_GRANTED message
        :return: None
        """
        self.__conn_to_view_observer.send(Payload(ViewObserver.MAP_INFO_REQUEST))

    @private
    @final
    def handle_map_info(self):
        """
        Handle the MAP_INFO message
        :return: None
        """

    @protected
    @final
    def idea_found(self, idea):
        """
        Must be called by a subclass every time a new idea is found
        :param idea: Idea
        :return: None
        """
        self.__current_idea = idea
        self.__idea_changed = True
        self.__choreographer_has_idea = False

    @property
    @protected
    def pathfinder_pause_requested(self):
        """
        Returns True if the pathfinding algorithm should be paused,
            and False otherwise
        :return: boolean
        """
        return self.__pathfinder_pause_requested.is_set()

    @protected
    def run_pathfinder_iteration(self):
        """
        Must be implemented by a subclass to run its pathfinding algorithm.
            The algorithm should periodically call the pathfinder_pause_requested
            method and stop if it returns True. The state of the search
            should be saved so that it will not restart when this method
            is called again
        :return: None
        """
        raise NotImplementedError("run_pathfinder_iteration method must be implemented")
