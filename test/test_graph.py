from unittest import TestCase
from pathlib import Path

from graph.core import Graph

class TestGraph(TestCase):
    def test_init_no_file(self):
        graph = Graph()
        self.assertEqual(graph.node_count, 0)
        self.assertEqual(graph.edge_count, 0)
        self.assertEqual(graph.nodes, [])
        self.assertEqual(graph.edges, [])
        
    def test_init_file(self):
        path = f"{Path.cwd()}/test/test-graphs/graph9.gra"
        graph = Graph(filename=path)
        # check if the graph was loaded correctly
        self.assertEqual(graph.node_count, 9)
        self.assertEqual(graph.edge_count, 9)
        self.assertEqual(graph.nodes[0].name, "A")
        self.assertEqual(graph.nodes[0].x_coord, 0.0)
        self.assertEqual(graph.nodes[0].y_coord, 0.0)
        self.assertEqual(graph.nodes[1].name, "B")
        self.assertEqual(graph.nodes[1].x_coord, 1.0)
        self.assertEqual(graph.nodes[1].y_coord, 0.0)
        self.assertEqual(graph.nodes[-1].name, "I")
        self.assertEqual(graph.nodes[-1].x_coord, 2.0)
        self.assertEqual(graph.nodes[-1].y_coord, 2.0)
        self.assertEqual(graph.edges[0].name, "AB")
        self.assertEqual(graph.edges[0].head, 0)
        self.assertEqual(graph.edges[0].tail, 1)
        self.assertEqual(graph.edges[1].name, "BC")
        self.assertEqual(graph.edges[1].head, 1)
        self.assertEqual(graph.edges[1].tail, 2)
        self.assertEqual(graph.edges[-1].name, "HI")
        self.assertEqual(graph.edges[-1].head, 7)
        self.assertEqual(graph.edges[-1].tail, 8)
        # check neighbours
        # TODO: check neighbours
