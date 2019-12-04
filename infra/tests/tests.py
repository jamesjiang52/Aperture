"""
File containing tests for the backend classes
"""

import unittest
import numpy as np

from utils import Action
from mapping import Map


class TestUtils(unittest.TestCase):
    """
    Test the functions/classes in utils
    """

    def test_action_one_shot(self):
        """
        Test the method is_one_shot in class Action
        """
        self.assertFalse(Action.MoveForward.is_one_shot())
        self.assertTrue(Action.Jump.is_one_shot())
        self.assertFalse(Action.CameraUp.is_one_shot())
        self.assertTrue(Action.Portal1.is_one_shot())
        self.assertTrue(Action.Interact.is_one_shot())


class TestMap(unittest.TestCase):
    """
    Test the Map class
    """

    def test_normalize(self):
        """
        Test the method normalize
        """
        self.assertTrue(np.array_equal(Map.normalize(np.array([1, 0, 0])),
                                       np.array([1, 0, 0])))
        self.assertTrue(np.array_equal(Map.normalize(np.array([3, 4, 12])),
                                       np.array([3 / 13, 4 / 13, 12 / 13])))
        self.assertRaises(ValueError, Map.normalize, (np.array([0, 0, 0]),))

    def test_positions_close(self):
        """
        Test the method are_positions_close
        """
        self.assertTrue(Map.are_positions_close(np.array([100, 100, 100]),
                                                np.array([100, 100, 110])))
        self.assertTrue(Map.are_positions_close(np.array([100, 102, 104]),
                                                np.array([100, 110, 110])))
        self.assertTrue(Map.are_positions_close(np.array([98, 102, 103]),
                                                np.array([102, 99, 97])))
        self.assertFalse(Map.are_positions_close(np.array([100, 111, 100]),
                                                 np.array([100, 100, 100])))
        self.assertFalse(Map.are_positions_close(np.array([104, 101, 99]),
                                                 np.array([97, 96, 105])))

    def test_orientations_close(self):
        """
        Test the method are_orientations_close
        """

    def test_point_on_surface(self):
        """
        Test the method is_point_on_surface
        """
        self.assertTrue(Map.is_point_on_surface(np.array([1, 1, 0]),
                                                np.array([[0, 5, 2],
                                                          [0, 0, 3],
                                                          [0, 0, 0]])))
        self.assertTrue(Map.is_point_on_surface(np.array([1, 1, 0]),
                                                np.array([[3, 0, -1, 0, 4],
                                                          [3, 2, 0, -3, -1],
                                                          [0, 0, 0, 0, 0]])))
        self.assertFalse(Map.is_point_on_surface(np.array([1, 1, 1]),
                                                 np.array([[-1, 1, 4, 4],
                                                           [3, -1, 0, 5],
                                                           [0, 0, 0, 0]])))
        self.assertFalse(Map.is_point_on_surface(np.array([3, -1, 0]),
                                                 np.array([[-1, 1, 4, 4],
                                                           [3, -1, 0, 5],
                                                           [0, 0, 0, 0]])))


if __name__ == '__main__':
    unittest.main()
