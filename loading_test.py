""" this module is used to test the loading of the graph data from a file"""

from graph import Graph


if __name__ == "__main__":
    path = "graph9.gra"
    graph = Graph(filename=path)
    print([node.__str__() for node in graph.nodes])
    print([edge.__str__() for edge in graph.edges])
