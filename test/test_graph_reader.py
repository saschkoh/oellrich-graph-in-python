from unittest import TestCase
from pathlib import Path

from graph.core import Node, Edge, GraphReader


class TestGraphReader(TestCase):
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
        path = f"{Path.cwd()}/test/test-graphs/graph9.gra"
        graph = GraphReader(path).read()
        # check if the graph was loaded correctly
        self.assertEqual(graph.name, "")
        self.assertEqual(graph.directed, False)
        self.assertEqual(
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
        )
        self.assertEqual(
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
        )
        self.assertEqual(graph.node_count, 9)
        self.assertEqual(graph.edge_count, 9)
