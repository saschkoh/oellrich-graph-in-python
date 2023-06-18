""" this module is used to test the loading of the graph data from a file"""


class Graph:
    """ class for a graph data structure """
    def __init__(self, directed: bool = True, filename: str = None):
        self.__directed = directed
        self.__number_of_nodes = 0
        self.__number_of_edges = 0
        self.__nodes = []
        self.__edges = []
        self.__forward_neighbours = []
        self.__backward_neighbours = []

        if filename is not None:
            if not isinstance(filename, str):
                raise TypeError("Graph: __init__(filename)", filename)
            self.load_from_file(filename)

    def load_from_file(self, filename: str):
        """ reads the graph from a file """
        with open(f"./test-graphs/{filename}", "r") as file:
            lines = [line.split("#")[0].strip() for line in file.readlines()]
            print(lines)


if __name__ == "__main__":
    path = "graph9.gra"
    graph = Graph(filename=path)

