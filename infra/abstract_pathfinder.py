"""
Provide the Pathfinder class
"""

import threading


class Pathfinder:
    """
    Abstract class to calculate paths and notify observer objects about
        next optimal actions
    """

    def __init__(self):
        """
        Initialize a Pathfinder object with no observers
        """
        self.path_observers = []
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

    def notify_add_action(self, action):
        """
        Send an add_action notification to every observer with the
            given action
        :param action: Action
        :return: None
        """
        for observer in self.path_observers:
            observer.add_action(action)

    def notify_remove_action(self, action):
        """
        Send a remove_action notification to every observer with
            the given action
        :param action: Action
        :return: None
        """
        for observer in self.path_observers:
            observer.remove_action(action)

    def add_observer(self, observer):
        """
        Set the given PathObserver object to receive notifications
        :param observer: PathObserver
        :return: None
        """
        self.path_observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove the given PathObserver object from receiving notifications,
            returning True if successful and False otherwise
        :param observer: PathObserver
        :return: boolean
        """
        try:
            self.path_observers.remove(observer)
            return True
        except ValueError:
            return False

    def get_observers(self):
        """
        Return the list of PathObserver objects currently receiving
            notifications
        :return: list of PathObservers
        """
        return self.path_observers

    def set_observers(self, observers):
        """
        Set the observers of this object to the given list of PathObserver
            objects, returning the previous list of observers
        :param observers: list of PathObservers
        :return: list of PathObservers
        """
        previous_observers = self.path_observers
        self.path_observers = observers
        return previous_observers

    def clear_observers(self):
        """
        Remove all PathObserver objects from receiving notifications,
            returning the previous list of observers
        :return: list of PathObservers
        """
        previous_observers = self.path_observers
        self.path_observers = []
        return previous_observers
