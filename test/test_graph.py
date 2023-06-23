"""
This module contains the unit tests for the Graph class.
"""
from unittest import TestCase

from graph.core import Graph, Node, Edge


class TestGraph(TestCase):
    """
    TestCase class for testing the Graph class.
    """
    # define nodes and edges for testing
    node_a = Node("A", 0, 0, 0)
    node_b = Node("B", 1, 0, 1)
    node_c = Node("C", 2, 0, 2)
    edge_ab = Edge("AB", node_a, node_b, 0, 0)
    edge_bc = Edge("BC", node_b, node_c, 1, 1)

    def test_init(self):
        graph = Graph()
        self.assertEqual(graph.name, "")
        self.assertEqual(graph.directed, True)
        self.assertEqual(graph.nodes, None)
        self.assertEqual(graph.edges, None)
        self.assertEqual(graph.node_count, 0)
        self.assertEqual(graph.edge_count, 0)

    def test_init_with_data(self):
        graph = Graph(
            directed=True,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        self.assertEqual(graph.name, "")
        self.assertEqual(graph.directed, True)
        self.assertEqual(graph.nodes[0].name, "A")
        self.assertEqual(graph.nodes[0].x_coord, 0)
        self.assertEqual(graph.nodes[0].y_coord, 0)
        self.assertEqual(graph.nodes[0].index, 0)
        self.assertEqual(graph.nodes[1].name, "B")
        self.assertEqual(graph.nodes[1].x_coord, 1)
        self.assertEqual(graph.nodes[1].y_coord, 0)
        self.assertEqual(graph.nodes[1].index, 1)
        self.assertEqual(graph.nodes[2].name, "C")
        self.assertEqual(graph.nodes[2].x_coord, 2)
        self.assertEqual(graph.nodes[2].y_coord, 0)
        self.assertEqual(graph.nodes[2].index, 2)
        self.assertEqual(graph.edges[0].name, "AB")
        self.assertEqual(graph.edges[0].head, self.node_a)
        self.assertEqual(graph.edges[0].tail, self.node_b)
        self.assertEqual(graph.edges[0].index, 0)
        self.assertEqual(graph.edges[1].name, "BC")
        self.assertEqual(graph.edges[1].head, self.node_b)
        self.assertEqual(graph.edges[1].tail, self.node_c)
        self.assertEqual(graph.edges[1].index, 1)
        self.assertEqual(graph.node_count, 3)
        self.assertEqual(graph.edge_count, 2)

    def test_node_by_name(self):
        graph = Graph(
            directed=True,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        self.assertEqual(
            graph.node_by_name("A"),
            self.node_a,
        )
        self.assertEqual(
            graph.node_by_name("B"),
            self.node_b,
        )
        self.assertEqual(
            graph.node_by_name("C"),
            self.node_c,
        )

    def test_edge_by_name(self):
        graph = Graph(
            directed=True,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        self.assertEqual(
            graph.edge_by_name("AB"),
            self.edge_ab,
        )
        self.assertEqual(
            graph.edge_by_name("BC"),
            self.edge_bc,
        )

    def test_init_neighbors_directed(self):
        graph = Graph(
            directed=True,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        graph.init_neighbors()
        self.assertEqual(len(graph.nodes[0].f_neighbors), 1)
        self.assertEqual(graph.nodes[0].f_neighbors, {self.node_b})
        self.assertEqual(len(graph.nodes[1].f_neighbors), 1)
        self.assertEqual(graph.nodes[1].f_neighbors, {self.node_c})
        self.assertEqual(len(graph.nodes[2].f_neighbors), 0)
        self.assertEqual(graph.nodes[2].f_neighbors, set())
        self.assertEqual(len(graph.nodes[0].b_neighbors), 0)
        self.assertEqual(graph.nodes[0].b_neighbors, set())
        self.assertEqual(len(graph.nodes[1].b_neighbors), 1)
        self.assertEqual(graph.nodes[1].b_neighbors, {self.node_a})
        self.assertEqual(len(graph.nodes[2].b_neighbors), 1)
        self.assertEqual(graph.nodes[2].b_neighbors, {self.node_b})

    def test_init_neighbors_undirected(self):
        graph = Graph(
            directed=False,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        graph.init_neighbors()
        self.assertEqual(
            graph.nodes[0].f_neighbors,
            graph.nodes[0].b_neighbors
        )
        self.assertEqual(
            graph.nodes[1].f_neighbors,
            graph.nodes[1].b_neighbors
        )
        self.assertEqual(
            graph.nodes[2].f_neighbors,
            graph.nodes[2].b_neighbors
        )
        self.assertEqual(graph.nodes[0].b_neighbors, {self.node_b})
        self.assertEqual(
            graph.nodes[1].b_neighbors,
            {self.node_a, self.node_c}
        )
        self.assertEqual(graph.nodes[2].b_neighbors, {self.node_b})

    def test_auto_name(self):
        graph = Graph(
            directed=True,
            nodes=[
                self.node_a,
                self.node_b,
                self.node_c,
            ],
            edges=[
                self.edge_ab,
                self.edge_bc,
            ],
        )
        self.assertEqual(
            graph.auto_name(),
            "graph_directed-True_3-nodes_2-edges"
        )
        graph.name = "test"
        self.assertEqual(graph.auto_name(), "test")
