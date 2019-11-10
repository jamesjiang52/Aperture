"""
Implementation of a SLAM algorithm in the context of Portal 2,
    along with a solution search algorithm
"""

import numpy as np

import utils
from abstract_view_observer import ViewObserver
from abstract_pathfinder import Pathfinder


class Map(ViewObserver, Pathfinder):
    """
    Class that receives notifications containing observations from the game,
        stores them internally, and determines the next best action to
        take based on all past observations
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """
        Initialize an empty Map object
        """
        super().__init__()

        self.frames_observed = 0
        self.time = 0

        self.entities = []
        self.entity_positions = None
        self.entity_orientations = None

        self.surfaces = []
        self.surface_positions = None
        self.surface_orientations = None

        self.references = []
        self.reference_positions = None

        self.last_observation = None

    # ------------------- BEGIN VIEWOBSERVER IMPLEMENTATION -------------------

    # Maximum magnitude of the difference between two position vectors
    # for them to be considered the same, to compensate for net
    # prediction error
    max_pos_diff = 10

    # Minimum cosine of the angle between two orientation vectors for
    # them to be considered the same, to compensate for net prediction
    # error
    min_or_cos_diff = 0.99

    # Maximum magnitude of the difference between two position vectors
    # in two different frames for them to be considered as referring
    # to the same object
    max_pos_offset = 20

    # Minimum cosine of the angle between two orientation vectors in
    # two different frames for them to be considered as referring to
    # the same object
    min_or_cos_offset = 0.97

    @staticmethod
    def normalize(arr):
        """
        Returns the given array normalized to have magnitude 1
        :param arr: 3D numpy array
        :return: 3D numpy array
        """
        norm = np.linalg.norm(arr)

        if norm == 0:
            raise ValueError("Array cannot be the zero vector")

        return arr / norm

    @staticmethod
    def are_positions_close(pos1, pos2, epsilon=max_pos_diff):
        """
        Returns True if pos1 is epsilon-close to pos2, otherwise False
        :param pos1: 3D numpy array
        :param pos2: 3D numpy array
        :param epsilon: float
        :return: boolean
        """
        return np.linalg.norm(pos1 - pos2) <= epsilon

    @staticmethod
    def are_orientations_close(or1, or2, epsilon=min_or_cos_diff):
        """
        Returns True if or1 is epsilon-close to or2, otherwise False
        :param or1: 3D numpy array
        :param or2: 3D numpy array
        :param epsilon: -1 <= float <= 1
        :return: boolean
        """
        return np.dot(Map.normalize(or1), Map.normalize(or2)) >= epsilon

    @staticmethod
    def is_point_on_surface(point, surface):
        """
        Returns True if the point is on the surface, otherwise False
        :param point: 3D numpy array
        :param surface: 3xn numpy matrix, where the n columns are the corner
            coordinates ordered by following the perimeter in either direction.
            Requires n >= 3 and surface is convex
        :return: boolean
        """
        surface_plane = surface[:, :3]
        normal = np.cross(surface_plane[:, 1] - surface_plane[:, 0],
                          surface_plane[:, 2] - surface_plane[:, 0])
        is_on_plane = np.dot(point - surface_plane[:, 0], normal) == 0

        if not is_on_plane:
            return False

        corner_1 = surface[:, 0]
        corner_2 = surface[:, 1]
        direction = np.cross(point - corner_1, corner_2 - corner_1)

        for i in range(1, surface.shape[1]):
            corner_1 = surface[:, i]
            corner_2 = surface[:, (i + 1) % surface.shape[1]]
            if np.dot(direction, np.cross(point - corner_1, corner_2 - corner_1)) < 0:
                return False

        return True

    @staticmethod
    def get_single_positional_update_matrices(old, new):
        """
        Returns a tuple of two matrices, the first of which
            is a 3x4 matrix used for updating position, and the
            second of which is a 3x3 matrix used for updating
            orientation.
        :param old: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            where the first entry is a position vector and the second and
            third entries are orientation vectors
        :param new: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            with the same specifications
        :return: (3x4 numpy array, 3x3 numpy array) tuple
        """
        old_or_1 = Map.normalize(old[1])
        old_or_2 = Map.normalize(old[2])
        new_or_1 = Map.normalize(new[1])
        new_or_2 = Map.normalize(new[2])

        gamma = np.linalg.inv(np.array([[new_or_1[0], -new_or_1[1]],
                                        [new_or_2[0], -new_or_2[1]]])) @ \
                np.array([old_or_1[0], old_or_2[0]])
        alpha = np.linalg.inv(np.array([[old_or_1[2], -old_or_1[1]],
                                        [old_or_2[2], -old_or_2[1]]])) @ \
                np.array([new_or_1[2], new_or_2[2]])

        rotation = np.array([[gamma[0], gamma[1] * alpha[0], gamma[1] * alpha[1]],
                             [-gamma[1], gamma[0] * alpha[0], gamma[0] * alpha[1]],
                             [0, -alpha[1], alpha[0]]])
        translation = np.append(np.identity(3), rotation.transpose() @ new[0] - old[0], axis=1)

        return rotation @ translation, rotation

    @staticmethod
    def get_double_positional_update_matrices(old, new):
        """
        Returns a tuple of two matrices, the first of which
            is a 3x4 matrix used for updating position, and the
            second of which is a 3x3 matrix used for updating
            orientation.
        :param old: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            where the first and second entries are position vectors and the
            third entry is an orientation vector
        :param new: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            with the same specifications
        :return: (3x4 numpy array, 3x3 numpy array) tuple
        """
        return Map.get_single_positional_update_matrices((old[0], old[2], old[0] - old[1]),
                                                         (new[0], new[2], new[0] - new[1]))

    @staticmethod
    def get_triple_positional_update_matrices(old, new):
        """
        Returns a tuple of two matrices, the first of which
            is a 3x4 matrix used for updating position, and the
            second of which is a 3x3 matrix used for updating
            orientation.
        :param old: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            where all entries are position vectors
        :param new: (3D numpy array, 3D numpy array, 3D numpy array) tuple,
            with the same specifications
        :return: (3x4 numpy array, 3x3 numpy array) tuple
        """
        return Map.get_single_positional_update_matrices((old[0], old[0] - old[1], old[1] - old[2]),
                                                         (new[0], new[0] - new[1], new[1] - new[2]))

    @staticmethod
    def are_same_entity(entity1, entity2):
        """
        Returns True if the two EntityObservation objects given refer
            to the same entity in two different frames, and False otherwise
        :param entity1: EntityObservation
        :param entity2: EntityObservation
        :return: boolean
        """
        if entity1.entity != entity2.entity:
            return False

        if not Map.are_positions_close(entity1.position,
                                       entity2.position,
                                       epsilon=Map.max_pos_offset):
            return False

        return Map.are_orientations_close(entity1.orientation,
                                          entity2.orientation,
                                          epsilon=Map.min_or_cos_offset)

    @staticmethod
    def are_same_references(reference1, reference2):
        """
        Returns True if the two ReferenceObservation objects given refer
            to the same reference in two different frames, and False otherwise
        :param reference1: ReferenceObservation
        :param reference2: ReferenceObservation
        :return: boolean
        """
        return Map.are_positions_close(reference1.position,
                                       reference2.position,
                                       epsilon=Map.max_pos_offset)

    def __filter_entities(self, entities):
        """
        Given a list of EntityObservations, return a new list containing
            all elements of the list that are not already in the map
        :param entities: list of EntityObservations
        :return: list of EntityObservation
        """
        filtered_entities = []
        for _e in entities:
            for j in range(len(self.entities)):
                if _e.entity == self.entities[j] and \
                        Map.are_positions_close(_e.position, self.entity_positions[:, j]) and \
                        Map.are_orientations_close(_e.orientation, self.entity_orientations[:, j]):
                    break
            else:
                filtered_entities.append(_e)

        return filtered_entities

    def __filter_references(self, references):
        """
        Given a list of ReferenceObservations, return a new list containing
            all elements of the list that are not already in the map
        :param references: list of ReferenceObservations
        :return: list of ReferenceObservations
        """
        filtered_references = []
        for _r in references:
            for j in range(len(self.references)):
                if Map.are_positions_close(_r.position, self.reference_positions[:, j]):
                    break
            else:
                filtered_references.append(_r)

        return filtered_references

    def __update_entities(self, position_update, orientation_update, new_entities):
        """
        Update the positions and orientations of all observed entities, and
            append the given new entities to them
        :param position_update: 3x4 numpy array
        :param orientation_update: 3x3 numpy array
        :param new_entities: iterable of EntityObservations
        :return: None
        """
        if self.entities:
            self.entity_positions = \
                position_update @ \
                np.vstack([self.entity_positions, np.ones(self.entity_positions.shape[1])])
            self.entity_orientations = orientation_update @ self.entity_orientations

        new_entities = self.__filter_entities(new_entities)

        for entity in new_entities:
            if self.entities:
                np.append(self.entity_positions, entity.position.reshape((3, 1)), axis=1)
                np.append(self.entity_orientations, entity.orientation.reshape((3, 1)), axis=1)
            else:
                self.entity_positions = entity.position.reshape((3, 1))
                self.entity_orientations = entity.orientation.reshape((3, 1))
            self.entities.append(entity.entity)

    def __update_surfaces(self, position_update, orientation_update, new_surfaces):
        """
        Update the positions and orientations of all observed surfaces, and
            append the given new surfaces to them
        TODO: figure out embedded surfaces
        :param position_update: 3x4 numpy array
        :param orientation_update: 3x3 numpy array
        :param new_surfaces: iterable of SurfaceObservations
        :return: None
        """
        if self.surfaces:
            self.surface_positions = \
                position_update @ \
                np.vstack([self.surface_positions, np.ones(self.surface_positions.shape[1])])
            self.surface_orientations = orientation_update @ self.surface_orientations

        for surface in new_surfaces:
            if self.surfaces:
                np.append(self.surface_positions, surface.corners, axis=1)
                np.append(self.surface_orientations, surface.orientation.reshape((3, 1)), axis=1)
            else:
                self.surface_positions = surface.corners
                self.surface_orientations = surface.orientation.reshape((3, 1))
            self.surfaces.append(surface.surface)

    def __update_references(self, position_update, new_references):
        """
        Update the positions of all observed references, and append the
            given new references to them
        :param position_update: 3x4 numpy array
        :param new_references: iterable of ReferenceObservations
        :return: None
        """
        if self.references:
            self.reference_positions = \
                position_update @ \
                np.vstack([self.reference_positions, np.ones(self.reference_positions.shape[1])])

        new_references = self.__filter_references(new_references)

        for reference in new_references:
            if self.references:
                np.append(self.reference_positions, reference.position.reshape((3, 1)), axis=1)
            else:
                self.reference_positions = reference.position.reshape((3, 1))
            self.references.append(reference.id)

    def __find_common_entities(self, new_entities):
        """
        Returns a list of 2-tuples of EntityObservations, where the first entry
            of every tuple is an EntityObservation in the last frame that refers
            to the same entity as the second entry in the tuple that is an
            EntityObservation in the given iterable
        :param new_entities: iterable of EntityObservations
        :return: list of (EntityObservation, EntityObservation) tuples
        """
        pairs = []
        for prev_observed_entity in self.last_observation[0]:
            for observed_entity in new_entities:
                if Map.are_same_entity(prev_observed_entity, observed_entity):
                    pairs.append((prev_observed_entity, observed_entity))
                    break

        return pairs

    def __find_common_references(self, new_references):
        """
        Returns a list of 2-tuples of ReferenceObservations, where the first
            entry of every tuple is a ReferenceObservation in the last frame
            that refers to the same reference as the second entry in the tuple
            that is a ReferenceObservation in the given iterable
        :param new_references: iterable of ReferenceObservations
        :return: list of (ReferenceObservation, ReferenceObservation) tuples
        """
        pairs = []
        for prev_observed_reference in self.last_observation[2]:
            for observed_reference in new_references:
                if Map.are_same_references(prev_observed_reference, observed_reference):
                    pairs.append((prev_observed_reference, observed_reference))
                    break

        return pairs

    def add_observation(self, entities, surfaces, references, time):
        """
        Add the given EntityObservations, SurfaceObservations, and
            ReferenceObservations to the map. This method makes the
            assumption that successive calls will be close together
            (implying bounded offset). The assumption that the player
            never rotates around the y-axis is also made.
        For mapping to work, we require that two consecutive frames have
            in common either:
                1. at least two entities
                2. at least one entity and at least one reference
                3. at least three references
            If none of these are satisfied, this method will throw
        :param entities: iterable of EntityObservation objects
        :param surfaces: iterable of SurfaceObservation objects
        :param references: iterable of ReferenceObservation objects
        :param time: float representing the time of the observation
        :return: None
        """

        self.frames_observed += 1

        # The very first frame observed; store the observations and return
        if not self.last_observation:
            self.__update_entities(None, None, entities)
            self.__update_surfaces(None, None, surfaces)
            self.__update_references(None, references)
            self.last_observation = [entities, surfaces, references]
            return

        e_common = self.__find_common_entities(entities)
        r_common = self.__find_common_references(references)

        if len(e_common) >= 2:
            position_update, orientation_update = Map.get_single_positional_update_matrices(
                (e_common[0][0].position, e_common[0][0].orientation, e_common[1][0].orientation),
                (e_common[0][1].position, e_common[0][1].orientation, e_common[1][1].orientation)
            )
        elif len(e_common) >= 1 and len(r_common) >= 1:
            position_update, orientation_update = Map.get_double_positional_update_matrices(
                (e_common[0][0].position, r_common[0][0].position, e_common[0][0].orientation),
                (e_common[0][1].position, r_common[0][1].position, e_common[0][1].orientation)
            )
        elif len(r_common) >= 3:
            position_update, orientation_update = Map.get_triple_positional_update_matrices(
                (r_common[0][0].position, r_common[1][0].position, r_common[2][0].position),
                (r_common[0][1].position, r_common[1][1].position, r_common[2][1].position)
            )
        else:
            raise ValueError("Not enough information given by parameters to update map")

        self.__update_entities(position_update, orientation_update, entities)
        self.__update_surfaces(position_update, orientation_update, surfaces)
        self.__update_references(position_update, references)

        self.last_observation = [entities, surfaces, references]
        self.time = time

    def get_player_position(self, confidence_window=None):
        """
        Must be implemented by a subclass to get the position of the
            player. If confidence_window is not None, the second return
            value will represent the error such that the probability that
            the actual player position is within the error is greater
            than the window.
        TODO
        :param confidence_window: 0 <= float <= 1 or None
        :return: (3D numpy array, 3D numpy array) tuple
        """
        return np.zeros(3), np.zeros(3)

    def get_player_orientation(self, confidence_window=None):
        """
        Must be implemented by a subclass to get the orientation of the
            player. If confidence_window is not None, the second return
            value will represent the error such that the probability that
            the actual player orientation is within the error is greater
            than the window.
        TODO
        :param confidence_window: 0 <= float <= 1 or None
        :return: (3D numpy array, 3D numpy array) tuple
        """
        return np.zeros(3), np.zeros(3)

    # ------------------- END VIEWOBSERVER IMPLEMENTATION -------------------

    # ------------------- BEGIN PATHFINDER IMPLEMENTATION -------------------

    def is_exit_found(self):
        """
        Returns true if the exit has been observed at least once, and
            false otherwise
        :return: boolean
        """
        return utils.Entity.Exit in self.entities

    def run_pathfinder(self, *args, **kwargs):
        """
        TODO: implement this
        :param args: arguments
        :param kwargs: keyword arguments
        :return: None
        """
