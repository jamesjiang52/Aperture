"""
Provide the ViewObserver class
"""


class ViewObserver:
    """
    Abstract class that receives notifications containing observations
        in a single frame from Portal 2
    """

    # pylint: disable=too-few-public-methods

    def add_observation(self, entities, surfaces, references):
        """
        Must be implemented by a subclass to handle observation events
        :param entities: iterable of EntityObservation objects
        :param surfaces: iterable of SurfaceObservation objects
        :param references: iterable of ReferenceObservation objects
        :return: None
        """
        raise NotImplementedError("add_observation method must be implemented")
