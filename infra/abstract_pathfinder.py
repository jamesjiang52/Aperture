"""
Provide the Pathfinder class
"""

import threading


class Pathfinder:
    """
    Abstract class to calculate paths and notify Choreographers
        about next ideas
    """

    def __init__(self):
        """
        Initialize a Pathfinder object with no observers
        """
        self.observers = []
        self.search_thread = None

    def start(self, *args, **kwargs):
        """
        Spawn a separate thread that runs the implementation of the
            pathfinding algorithm
        :return: None
        """
        self.search_thread = threading.Thread(target=self.run_pathfinder, args=args, kwargs=kwargs)
        self.search_thread.start()

    def run_pathfinder(self, *args, **kwargs):
        """
        Run the pathfinding algorithm
        :return: None
        """
        raise NotImplementedError("run_pathfinder method must be implemented")

    def notify_observers(self, idea):
        """
        Call notify_idea on every observer with the given idea
        :param idea: Idea
        :return: None
        """
        for observer in self.observers:
            observer.notify_idea(idea)

    def add_observer(self, observer):
        """
        Set the given Choreographer object to receive notifications
        :param observer: Choreographer
        :return: None
        """
        self.observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove the given Choreographer object from receiving notifications,
            returning True if successful and False otherwise
        :param observer: Choreographer
        :return: boolean
        """
        try:
            self.observers.remove(observer)
            return True
        except ValueError:
            return False

    def get_observers(self):
        """
        Return the list of Choreographer objects currently receiving
            notifications
        :return: list of Choreographers
        """
        return self.observers

    def clear_observers(self):
        """
        Remove all Choreographer objects from receiving notifications,
            returning the previous list of observers
        :return: list of Choreographers
        """
        previous_observers = self.observers
        self.observers = []
        return previous_observers
