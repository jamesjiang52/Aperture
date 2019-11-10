"""
Provide the Choreographer class
"""


class Choreographer:
    """
    Abstract class to carry out ideas sent by Pathfinder objects by
        making decisions on what action to take based on current map
        observations
    """

    def __init__(self, view_observer=None, pathfinder=None):
        """
        Initialize a choreographer object with the given ViewObserver
            and Pathfinder objects
        :param view_observer: ViewObserver to query view information from
        :param pathfinder: Pathfinder to receive ideas from
        """
        self.view_observer = view_observer
        self.pathfinder = pathfinder

    def set_view_observer(self, view_observer):
        """
        Set this Choreographer object to query view information from
            the ViewObserver object given
        :param view_observer: ViewObserver or None
        :return: None
        """
        self.view_observer = view_observer

    def set_pathfinder(self, pathfinder):
        """
        Set this Choreographer object to receive notifications from
            the Pathfinder object given
        :param pathfinder: Pathfinder or None
        :return: None
        """
        self.pathfinder = pathfinder

    def notify_idea(self, idea):
        """
        Must be implemented by a subclass to handle notification events
        :param idea: Idea
        :return: None
        """
        raise NotImplementedError("notify_idea method must be implemented")
