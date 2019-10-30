"""
Provide the PathObserver class
"""


class PathObserver:
    """
    Abstract class to receive notifications from a Pathfinder object
    """

    def add_action(self, action):
        """
        Handle an addition of the given action
        :param action: Action
        :return: None
        """
        raise NotImplementedError("add_action method must be implemented")

    def remove_action(self, action):
        """
        Handle a removal of the given action
        :param action: Action
        :return: None
        """
        raise NotImplementedError("remove_action method must be implemented")
