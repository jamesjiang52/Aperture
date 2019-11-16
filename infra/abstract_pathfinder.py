"""
Provide the Pathfinder class
"""

from utils import Payload
from abstract_view_observer import ViewObserver
from abstract_choreographer import Choreographer


class Pathfinder:
    """
    Abstract class to calculate paths and notify Choreographers
        about next ideas
    """

    PAUSE_GRANTED = 11
    MAP_INFO = 12

    def __init__(self, conn_to_view_observer, conn_to_choreographer):
        """
        Initialize a Pathfinder with the given connections to a
            ViewObserver object and a Choreographer object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_choreographer: multiprocessing.Connection
        """
        self.conn_to_view_observer = conn_to_view_observer
        self.conn_to_choreographer = conn_to_choreographer

    def main(self):
        """
        Main entry point
        :return: None
        """
        self.run_pathfinder()

    def request_pause(self):
        self.conn_to_choreographer.send(Payload(Choreographer.PAUSE_REQUEST))

    def allow_resume(self):
        self.conn_to_choreographer.send(Payload(Choreographer.RESUME))

    def __handle_pause_granted(self):
        self.conn_to_view_observer.send(Payload(ViewObserver.MAP_INFO_REQUEST))

    def run_pathfinder(self):
        """
        Run the pathfinding algorithm
        :return: None
        """
        raise NotImplementedError("run_pathfinder method must be implemented")
