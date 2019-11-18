"""
Provide the ViewObserver class
"""

from ..Qualifiers.qualifiers import qualify, private, public, final
from utils import Payload
from abstract_pathfinder import Pathfinder
from abstract_choreographer import Choreographer


@qualify
class ViewObserver:
    """
    Abstract class that receives notifications containing observations
        in a single frame from Portal 2
    """

    PLAYER_INFO_REQUEST = 21
    MAP_INFO_REQUEST = 22

    @public
    def __init__(self, conn_to_pathfinder, conn_to_choreographer):
        """
        Initialize a ViewObserver with the given connections to a
            Pathfinder object and a Choreographer object
        :param conn_to_pathfinder: multiprocessing.Connection
        :param conn_to_choreographer: multiprocessing.Connection
        """
        self.conn_to_pathfinder = conn_to_pathfinder
        self.conn_to_choreographer = conn_to_choreographer

    @public
    @final
    def main(self):
        """
        Main entry point
        :return: None
        """

    @private
    @final
    def handle_player_info_request(self):
        """
        Handle the PLAYER_INFO_REQUEST message
        :return: None
        """
        player_info = (self.get_player_position(), self.get_player_orientation())
        self.conn_to_choreographer.send(Payload(Choreographer.PLAYER_INFO, player_info))

    @private
    @final
    def handle_map_info_request(self):
        """
        Handle the MAP_INFO_REQUEST message
        :return: None
        """
        map_info = self.get_chamber_state()
        self.conn_to_pathfinder.send(Payload(Pathfinder.MAP_INFO, map_info))

    @public
    def add_observation(self, entities, surfaces, references, time):
        """
        Must be implemented by a subclass to handle observation events
        :param entities: iterable of EntityObservation objects
        :param surfaces: iterable of SurfaceObservation objects
        :param references: iterable of ReferenceObservation objects
        :param time: float representing the time of the observation
        :return: None
        """
        raise NotImplementedError("add_observation method must be implemented")

    @public
    def get_chamber_state(self):
        """
        Must be implemented by a subclass to return information about
            all entities, surfaces, and references that have been observed.
        :return: (list of EntityObservations, list of SurfaceObservations,
            list of ReferenceObservations) tuple
        """
        raise NotImplementedError("get_chamber_state method must be implemented")

    @public
    def get_player_position(self, confidence_window=None):
        """
        Must be implemented by a subclass to get the position of the
            player. If confidence_window is not None, the second return
            value will represent the error such that the probability that
            the actual player position is within the error is greater
            than the window.
        :param confidence_window: 0 <= float <= 1 or None
        :return: (3D numpy array, 3D numpy array) tuple
        """
        raise NotImplementedError("get_player_position method must be implemented")

    @public
    def get_player_orientation(self, confidence_window=None):
        """
        Must be implemented by a subclass to get the orientation of the
            player. If confidence_window is not None, the second return
            value will represent the error such that the probability that
            the actual player orientation is within the error is greater
            than the window.
        :param confidence_window: 0 <= float <= 1 or None
        :return: (3D numpy array, 3D numpy array) tuple
        """
        raise NotImplementedError("get_player_orientation method must be implemented")
