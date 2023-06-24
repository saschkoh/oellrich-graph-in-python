"""
This module contains the unit tests for the Node class.
"""
from unittest import TestCase

from oellrich_graph.core import Node


class TestNode(TestCase):
    """
    TestCase class for testing the Node class.
    """
    def test_create_empty_node(self):
        node = Node()
        self.assertEqual(node.name, None)
        self.assertEqual(node.x_coord, None)
        self.assertEqual(node.y_coord, None)
        self.assertEqual(node.index, None)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, set())
        self.assertEqual(node.b_neighbors, set())

    def test_load_from_string_int(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        self.assertEqual(node.name, "A")
        self.assertEqual(node.x_coord, 0)
        self.assertEqual(node.y_coord, 0)
        self.assertEqual(node.index, 0)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, set())
        self.assertEqual(node.b_neighbors, set())

    def test_load_from_string_float(self):
        node = Node()
        node.load_from_string("test 2.3 3.14159", 500)
        self.assertEqual(node.name, "test")
        self.assertEqual(node.x_coord, 2.3)
        self.assertEqual(node.y_coord, 3.14159)
        self.assertEqual(node.index, 500)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, set())
        self.assertEqual(node.b_neighbors, set())

    def test_load_from_str_to_set_node(self):
        node = Node("A")
        with self.assertRaisesRegex(ValueError, "is already set"):
            node.load_from_string("A 0 0", 0)
        node = Node("A", 0, 0, 0, 0)
        with self.assertRaisesRegex(ValueError, "is already set"):
            node.load_from_string("A 0 0", 0)

    def test_load_from_invalid_str(self):
        node = Node()
        with self.assertRaisesRegex(ValueError, "incorrect format"):
            node.load_from_string("A 0", 0)

    def test_allowed(self):
        node = Node()
        self.assertFalse(node.allowed)
        node.load_from_string("A 0 0", 0)
        self.assertTrue(node.allowed)

    def test_not_allowed(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        node.name = None
        self.assertFalse(node.allowed)

    def test_str_0(self):
        node = Node()
        node.load_from_string("A", 0)
        self.assertEqual(str(node), "Object type: Node, name: A, index: 0")

    def test_str_1(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        self.assertEqual(
            str(node),
            "Object type: Node, name: A, x_coord: 0.0, y_coord: 0.0, index: 0"
        )

    def test_str_2(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        node.weight = 1.0
        self.assertEqual(
            str(node),
            "Object type: Node, name: A, x_coord: 0.0, y_coord: 0.0, index: 0, weight: 1.0"
        )

    def test_clear(self):
        node = Node("A", 1, 2, 3, 4)
        node.f_neighbors.add(Node("B", 5, 6, 7, 8))
        node.b_neighbors.add(Node())
        node.clear()
        self.assertEqual(node.name, None)
        self.assertEqual(node.x_coord, None)
        self.assertEqual(node.y_coord, None)
        self.assertEqual(node.index, 3)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, set())
        self.assertEqual(node.b_neighbors, set())
