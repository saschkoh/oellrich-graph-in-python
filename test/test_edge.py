"""
This module contains the unit tests for the Edge class.
"""
from unittest import TestCase

from graph.core import Node, Edge


class TestEdge(TestCase):
    """
    TestCase class for testing the Edge class.
    """
    # define a global dict for nodes
    nodes = {
        "A": Node("A", 0, 0, 0),
        "B": Node("B", 1, 2, 1),
    }

    def test_create_empty_edge(self):
        edge = Edge()
        self.assertEqual(edge.name, None)
        self.assertEqual(edge.head, None)
        self.assertEqual(edge.tail, None)
        self.assertEqual(edge.index, None)
        self.assertEqual(edge.weight, None)

    def test_load_from_string(self):
        edge = Edge()
        edge.load_from_string("AB A B", self.nodes, 0)
        self.assertEqual(edge.name, "AB")
        self.assertEqual(edge.head, self.nodes["A"])
        self.assertEqual(edge.tail, self.nodes["B"])
        self.assertEqual(edge.index, 0)
        self.assertEqual(edge.weight, None)

    def test_load_from_string_to_set_edge(self):
        edge = Edge("AB")
        with self.assertRaisesRegex(ValueError, "is already set"):
            edge.load_from_string("AB A B", self.nodes, 0)
        edge = Edge("AB", self.nodes["A"], self.nodes["B"], 0, 0)
        with self.assertRaisesRegex(ValueError, "is already set"):
            edge.load_from_string("AB A B", self.nodes, 0)

    def test_load_from_invalid_string_1(self):
        edge = Edge()
        with self.assertRaisesRegex(ValueError, "incorrect format"):
            edge.load_from_string("AB A", self.nodes, 0)

    def test_load_from_invalid_string_2(self):
        edge = Edge()
        with self.assertRaisesRegex(ValueError, "incorrect format"):
            edge.load_from_string("AB A B C", self.nodes, 0)

    def test_allowed(self):
        edge = Edge()
        self.assertFalse(edge.allowed)
        edge.load_from_string("AB A B", self.nodes, 0)
        self.assertTrue(edge.allowed)

    def test_not_allowed(self):
        edge = Edge()
        self.assertFalse(edge.allowed)
        edge.load_from_string("AB A B", self.nodes, 0)
        edge.name = None
        self.assertFalse(edge.allowed)

    def test_str_0(self):
        edge = Edge()
        edge.load_from_string("AB A B", self.nodes, 0)
        self.assertEqual(
            str(edge),
            "Object type: Edge, name: AB, head: A, tail: B, index: 0"
        )

    def test_str_1(self):
        edge = Edge()
        edge.load_from_string("AB A B", self.nodes, 0)
        edge.weight = 1.0
        self.assertEqual(
            str(edge),
            "Object type: Edge, name: AB, head: A, tail: B, index: 0, weight: 1.0"
        )

    def test_clear(self):
        edge = Edge()
        edge.load_from_string("AB A B", self.nodes, 3)
        edge.clear()
        self.assertEqual(edge.name, None)
        self.assertEqual(edge.head, None)
        self.assertEqual(edge.tail, None)
        self.assertEqual(edge.index, 3)
        self.assertEqual(edge.weight, None)
