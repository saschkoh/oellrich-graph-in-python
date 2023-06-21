from unittest import TestCase

from graph.core import Node


class TestGraph(TestCase):
    def test_create_empty_node(self):
        node = Node()
        self.assertEqual(node.name, None)
        self.assertEqual(node.x_coord, None)
        self.assertEqual(node.y_coord, None)
        self.assertEqual(node.index, None)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, [])
        self.assertEqual(node.b_neighbors, [])

    def test_load_from_string_int(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        self.assertEqual(node.name, "A")
        self.assertEqual(node.x_coord, 0)
        self.assertEqual(node.y_coord, 0)
        self.assertEqual(node.index, 0)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, [])
        self.assertEqual(node.b_neighbors, [])

    def test_load_from_string_float(self):
        node = Node()
        node.load_from_string("test 2.3 3.14159", 500)
        self.assertEqual(node.name, "test")
        self.assertEqual(node.x_coord, 2.3)
        self.assertEqual(node.y_coord, 3.14159)
        self.assertEqual(node.index, 500)
        self.assertEqual(node.weight, None)
        self.assertEqual(node.f_neighbors, [])
        self.assertEqual(node.b_neighbors, [])

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
        self.assertTrue(node.allowed)
        node.load_from_string("A 0 0", 0)
        self.assertTrue(node.allowed)

    def test_not_allowed(self):
        node = Node()
        node.load_from_string("A 0 0", 0)
        node.name = ""
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
