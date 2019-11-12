"""
Utility functions and classes for the Map class
"""

from collections import namedtuple


Observation = namedtuple('Observation', ['entity_observations',
                                         'surface_observations',
                                         'reference_observations'])
Observation.__doc__ = """
                      Data class that represents all observations in a single frame
                      :param entity_observations: iterable of EntityObservations
                      :param surface_observations: iterable of SurfaceObservations
                      :param reference_observations: iterable of ReferenceObservations
                      """

TimedObservation = namedtuple('TimedObservation', ['observation', 'time'])
TimedObservation.__doc__ = """
                           Data class that represents an observation at a specific
                               time
                           :param observation: Observation
                           :param time: float
                           """


class EntityInstance:
    """
    Represents a specific instance of an Entity
    """

    def __init__(self, entity):
        """
        Initialize an EntityInstance of the specified entity
            with an unknown effect
        :param entity: Entity
        """
        self.entity = entity
        self.effect = None

    def set_effect(self, before, *after):
        """
        Set the effect of the EntityInstance. An effect is a broad term for
            any change in the state of a chamber shortly after an action
            is performed.
        :param before: Observation, representing the state before this
            Entity was interacted with
        :param after: TimedObservations, each representing the state after
            this Entity was interacted with, with the time component measured
            relative to the time of the interaction
        :return: None
        """
        if not self.entity.has_effect():
            raise ValueError(f"Effect cannot be set for entity of type {self.entity.value}")

        self.effect = (before, *after)

    def needs_exploration(self):
        """
        Returns True if the EntityInstance has an effect that has not been
            set (discovered) yet, and False otherwise
        :return: boolean
        """
        return self.entity.has_effect() and self.effect is None
