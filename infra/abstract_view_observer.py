"""
Provide the ViewObserver class
"""


class ViewObserver:
    """
    Abstract class that receives notifications containing observations
        in a single frame from Portal 2
    """

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
