"""
A concrete implementation of a Pathfinder
"""

from multiprocessing.connection import Connection

import numpy as np

from ..Qualifiers.qualifiers import qualify, private, protected, public, final
import utils
from abstract_pathfinder import Pathfinder


@qualify
class CPathfinder(Pathfinder):
    """
    Implementation of a Pathfinder class
    """

    @public
    @final
    def __init__(self, conn_to_view_observer: Connection, conn_to_choreographer: Connection):
        super().__init__(conn_to_view_observer, conn_to_choreographer)

        self.__current_map = None

        self.__exit_found_store = False

    @protected
    @final
    def is_exit_found(self):
        if self.__exit_found_store:
            return True

        if any(map(lambda observation: observation.entity == utils.Entity.Exit,
                   self.__current_map.entity_observations)):
            self.__exit_found_store = True
            return True

        return False
