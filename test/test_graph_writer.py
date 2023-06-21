"""
This module contains the unit test(s) for the GraphWriter class.
"""
from unittest import TestCase
from pathlib import Path

from graph.core import GraphReader, GraphWriter


class TestGraphWriter(TestCase):
    """
    TestCase class for testing the GraphWriter class.
    """
    def test_read_and_write(self):
        """
        Tests that a graph can be read from a file and replicated in a new file.
        """
        # read graph from file
        graph = GraphReader("test/test-graphs/graph9.gra").read()
        # delete old file if it exists
        if Path("test/graph9-copy.gra").exists():
            Path("test/graph9-copy.gra").unlink()
        # write graph to new file
        GraphWriter(graph, "test/graph9-copy.gra").write()
        # compare the two files
        path_1 = f"{Path.cwd()}/test/test-graphs/graph9.gra"
        path_2 = f"{Path.cwd()}/test/graph9-copy.gra"
        with open(path_1, "r", encoding="utf-8") as file1:
            with open(path_2, "r", encoding="utf-8") as file2:
                self.assertEqual(file1.read(), file2.read())
