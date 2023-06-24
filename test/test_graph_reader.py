"""
This module contains the unit tests for the GraphReader class.
"""
from unittest import TestCase
from pathlib import Path

from oellrich_graph.core import Node, Edge, GraphReader


def compare_nodes(node1, node2):
    """
    Compares all attributes of two nodes and returns True if they are equal.
    """
    return all([
        node1.name == node2.name,
        node1.x_coord == node2.x_coord,
        node1.y_coord == node2.y_coord,
        node1.index == node2.index,
        node1.weight == node2.weight,
        node1.f_neighbors == node2.f_neighbors,
        node1.b_neighbors == node2.b_neighbors,
    ])


def compare_node_lists(list1, list2):
    """
    Compares nodes of same index in two lists and returns True if all are equal.
    """
    return all(
        (compare_nodes(node1, node2) for node1, node2 in zip(list1, list2))
    )


def compare_edges(edge1, edge2):
    """
    Compares all attributes of two edges and returns True if they are euqal.
    """
    return all((
        edge1.name == edge2.name,
        edge1.head.name == edge2.head.name,
        edge1.tail.name == edge2.tail.name,
        edge1.index == edge2.index,
        edge1.weight == edge2.weight,
    ))


def compare_edge_lists(list1, list2):
    """
    Compares edges of the same index in two lists and returns True if all are equal.
    """
    return all(
        (compare_edges(edge1, edge2) for edge1, edge2 in zip(list1, list2))
    )


class TestGraphReader(TestCase):
    """
    TestCase class for testing the GraphReader class.
    """
    # define nodes and edges for testing
    node_a = Node("A", 0, 0, 0)
    node_b = Node("B", 1, 0, 1)
    node_c = Node("C", 2, 0, 2)
    node_d = Node("D", 0, 1, 3)
    node_e = Node("E", 1, 1, 4)
    node_f = Node("F", 2, 1, 5)
    node_g = Node("G", 0, 2, 6)
    node_h = Node("H", 1, 2, 7)
    node_i = Node("I", 2, 2, 8)
    edge_ab = Edge("AB", node_a, node_b, 0)
    edge_bc = Edge("BC", node_b, node_c, 1)
    edge_ad = Edge("AD", node_a, node_d, 2)
    edge_ae = Edge("AE", node_a, node_e, 3)
    edge_be = Edge("BE", node_b, node_e, 4)
    edge_dg = Edge("DG", node_d, node_g, 5)
    edge_eg = Edge("EG", node_e, node_g, 6)
    edge_fi = Edge("FI", node_f, node_i, 7)
    edge_hi = Edge("HI", node_h, node_i, 8)

    def test_with_file(self):
        """
        Tests if the GraphReader class extract the graph from a file successfully.
        """
        path = f"{Path.cwd()}/test/test-graphs/graph9.gra"
        graph = GraphReader(path).read()
        # check if the graph was loaded correctly
        self.assertEqual(graph.name, "")
        self.assertEqual(graph.directed, False)
        self.assertTrue(compare_node_lists(
            graph.nodes,
            [
                self.node_a,
                self.node_b,
                self.node_c,
                self.node_d,
                self.node_e,
                self.node_f,
                self.node_g,
                self.node_h,
                self.node_i,
            ]
        ))
        self.assertTrue(compare_edge_lists(
            graph.edges,
            [
                self.edge_ab,
                self.edge_bc,
                self.edge_ad,
                self.edge_ae,
                self.edge_be,
                self.edge_dg,
                self.edge_eg,
                self.edge_fi,
                self.edge_hi,
            ]
        ))
        self.assertEqual(graph.node_count, 9)
        self.assertEqual(graph.edge_count, 9)
