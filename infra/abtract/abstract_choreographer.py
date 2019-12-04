"""
Provide the Choreographer class
"""

from typing import Tuple
from threading import Thread, RLock
from multiprocessing.connection import Connection

import numpy as np

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
from utils import Payload, Idea
from abstract_view_observer import ViewObserver


@qualify
class Choreographer:
    """
    Abstract class to carry out ideas sent by Pathfinder objects by
        making decisions on what action to take based on current map
        observations
    """

    # --------------------------------- PUBLIC STATIC FIELDS ---------------------------------- #

    NEW_IDEA = 3
    PLAYER_INFO = 4

    # --------------------------------- CONSTRUCTOR ------------------------------------------- #

    @public
    def __init__(self, conn_to_view_observer: Connection, conn_to_pathfinder: Connection):
        """
        Initialize a Choreographer with the given connections to a
            ViewObserver object and a Pathfinder object
        :param conn_to_view_observer: multiprocessing.Connection
        :param conn_to_pathfinder: multiprocessing.Connection
        """
        self.__conn_to_view_observer = conn_to_view_observer
        self.__conn_to_pathfinder = conn_to_pathfinder

        self.__choreographer_thread = None
        self.__player_lock = RLock()
        self.__idea_lock = RLock()

        self.__player_info_requested = False
        self.__player_info = None

        self.__current_idea = None

    # --------------------------------- MAIN EVENT LOOP ---------------------------------------- #

    @public
    @final
    def main(self) -> None:
        """
        Main entry point
        :return: None
        """
        self.__choreographer_thread = Thread(target=self.run_choreography)
        self.__choreographer_thread.start()

        while True:
            self.request_player_info()

            while self.__conn_to_pathfinder.poll():
                payload = self.__conn_to_pathfinder.recv()
                {
                    Choreographer.NEW_IDEA: self.handle_new_idea
                }[payload.code](payload)

            payload = self.__conn_to_view_observer.recv()
            {
                Choreographer.PLAYER_INFO: self.handle_player_info
            }[payload.code](payload)

    # --------------------------------- HELPER FUNCTIONS -------------------------------------- #

    @private
    @final
    def handle_new_idea(self, payload: Payload) -> None:
        """
        Handle the NEW_IDEA message
        :param payload: Payload
        :return: None
        """
        with self.__idea_lock:
            self.__current_idea = payload.data

    @private
    @final
    def handle_player_info(self, payload: Payload) -> None:
        """
        Handle the PLAYER_INFO message
        :param payload: Payload
        :return: None
        """
        with self.__player_lock:
            if self.__player_info_requested:
                self.__player_info = payload.data
                self.__player_info_requested = False

    @private
    @final
    def request_player_info(self) -> None:
        """
        Request player info from the ViewObserver
        :return: None
        """
        if not self.__player_info_requested:
            self.__conn_to_view_observer.send(Payload(ViewObserver.PLAYER_INFO_REQUEST))
            self.__player_info_requested = True

    # --------------------------------- SUBCLASS INTERFACE ------------------------------------ #

    @property
    @protected
    def player_info(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get player info
        """
        with self.__player_lock:
            return self.__player_info

    @property
    @protected
    def idea(self) -> Idea:
        """
        Get the current idea
        """
        with self.__idea_lock:
            return self.__current_idea

    # --------------------------------- ABSTRACT METHODS -------------------------------------- #

    @protected
    def run_choreography(self) -> None:
        """
        Start managing interactions between the player and the game. This
            method can make use of self.player_info to get the most
            recent player info and self.idea to get the most recent idea.
        :return: None
        """
        raise NotImplementedError("run_choreography method must be implemented")
