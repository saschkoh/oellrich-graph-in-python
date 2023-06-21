"""
This module contains the core classes for the graph data structure. The
classes can be used to construct a graph from a file or to construct a graph
manually.
"""
from functools import lru_cache

# TODO
# - change entire structure: GraphReader --> attributes, Nodes, Edges --> Graph
#   when creating the Node objects, create hash table for the names
#   hand over Node objects to Edge objects
# - fix comments
# - add type hints
# - add logging
# - add tests


class Node:
    """
    Class for representing a node and its optional coordinates and weight. The
    class can be constructed with or without parameters. If no parameters are
    given, the load_from_string method can be used as an alternative constructor.
    """
    def __init__(
            self,
            name: str = None,
            x_coord: float = None,
            y_coord: float = None,
            index: int = None,
            weight: float = None
    ) -> None:
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.index = index
        self.weight = weight
        self.f_neighbors = []
        self.b_neighbors = []

    def load_from_string(self, string: str, index: int) -> None:
        """
        This method can be used as an alternative constructor. It takes a string
        of the format "name x_coord y_coord weight" and sets the corresponding
        parameters of the node object. If any of the parameters are already set,
        the method will raise an exception.
        """
        # check if any of the parameters are already set
        for param in [self.name, self.x_coord, self.y_coord, self.weight]:
            if param is not None:
                raise ValueError(
                    f"Node: load_from_string() parameter {param} is already set!"
                )
        # split the string into its components
        components = string.split(" ")
        # check if the string has the correct format
        if len(components) != 3:
            raise ValueError(
                f"Node: load_from_string() string {string} has incorrect format!"
            )
        self.name = components[0]
        self.x_coord = float(components[1])
        self.y_coord = float(components[2])
        self.index = index

    @property
    def allowed(self) -> bool:
        """ returns whether the node got deleted or not """
        return self.name != ""

    def __str__(self) -> str:
        """
        Prints and returns relevant information about the node. The x and y
        coordinates are not relevant for the graph structure.
        """
        out_string = self.name
        if self.weight is not None:
            out_string += f" [{self.weight}]"
        return out_string


class Edge:
    """
    Class for representing an edge and the node indices it connects to. The
    class can be constructed with or without parameters. If no parameters are
    specified, the load_from_string method can be used as an alternative
    constructor.
    """
    def __init__(
            self,
            name: str = None,
            head: Node = None,
            tail: Node = None,
            index: int = None,
            weight: float = None
    ) -> None:
        self.name = name
        self.head = head
        self.tail = tail
        self.index = index
        self.weight = weight

    def load_from_string(self, string: str, nodes_dict: dict[str, Node], index: int) -> None:
        """
        This method can be used as an alternative constructor. It takes a string
        of the format "name head_name tail_name" and sets the corresponding
        parameters of the edge object. If any of the parameters are already set,
        the method will raise an exception.
        """
        # check if any of the parameters are already set
        for param in [self.name, self.head, self.tail, self.weight]:
            if param is not None:
                raise ValueError(
                    f"Edge: load_from_string() parameter {param} is already set!"
                )
        # split the string into its components
        components = string.split(" ")
        # check if the string has the correct format
        if len(components) != 3:
            raise ValueError(
                f"Edge: load_from_string() string {string} has incorrect format!"
            )
        # set the parameters
        self.name = components[0]
        # in order to get the index of a node, we need to look it up in the
        # nodes list. This is done by the graph class.
        self.head = nodes_dict[components[1]]
        self.tail = nodes_dict[components[2]]
        self.index = index

    @property
    def allowed(self) -> bool:
        """
        returns whether the edge got deleted or not
        """
        return self.name != ""

    def __str__(self) -> str:
        """
        prints and returns relevant information about the edge
        """
        out_string = f"{self.name} ({self.head}, {self.tail})"
        if self.weight is not None:
            out_string += f" [{self.weight}]"
        return out_string


class Graph:
    """
    Class for a graph data structure translation of the graph class
    from the C++ implementation of Martin Oellrich
    """
    def __init__(
        self,
        name: str = "",
        directed: bool = True,
        nodes: list[Node] = None,
        edges: list[Edge] = None
    ):
        self.name = name
        self.directed = directed
        self.nodes = nodes
        self.edges = edges
        self.node_count = len(self.nodes)
        self.edge_count = len(self.edges)

    def node_by_name(self, name: str) -> Node:
        """
        Returns the node with the given name.
        """
        # TODO: this is a linear search, maybe use a dictionary instead
        for node in self.nodes:
            if node.name == name:
                return node
        raise ValueError(f"Graph: node_by_name(name), Node {name} not found!")

    def edge_by_name(self, name: str) -> Edge:
        """
        Returns the Edge object with a given name
        """
        # TODO: this is a linear search, maybe use a dictionary instead
        for edge in self.edges:
            if edge.name == name:
                return edge
        raise ValueError(f"Graph: edge_by_name(name), Edge {name} not found!")

    def init_neighbors(self) -> None:
        """
        Searches the edges for forward and backward neighbors and stores them
        in the corresponding lists of the nodes.
        """
        for edge in self.edges:
            edge.head.f_neighbors.append(edge.tail)
            if self.directed:
                edge.tail.b_neighbors.append(edge.head)
        if not self.directed:
            for node in self.nodes:
                node.b_neighbors = node.f_neighbors

    def auto_name(self) -> None:
        """
        Creates a name for the graph based on the names of the nodes and edges.
        """
        if self.name == "":
            return f"graph_directed-{self.directed}_{self.node_count}-nodes_{self.edge_count}-edges"
        return self.name


class GraphReader:
    """
    Class for loading and reading the file containing the graph data
    """
    def __init__(self, path: str) -> None:
        self.path = path
        self.node_count = None
        self.edge_count = None
        self.directed_raw = None
        self.nodes_raw = None
        self.edges_raw = None

    @property
    def directed(self) -> bool:
        """
        Returns whether the graph is directed or not. The directedness is
        saved as a string in the file.
        """
        if self.directed_raw in ["ungerichtet", "undirected", "u", "U"]:
            return False
        if self.directed_raw in ["gerichtet", "directed", "g", "G"]:
            return True
        raise ValueError(f"Directedness not specified correctly in file {self.path}")

    @lru_cache
    def nodes_dict(self) -> dict[str, Node]:
        """
        Creates a dictionary with the node names as keys and the node objects as
        values.
        """
        nodes_dict = {}
        for i, node_string in enumerate(self.nodes_raw):
            node = Node()
            node.load_from_string(node_string, i)
            nodes_dict[node.name] = node
        return nodes_dict

    @property
    def nodes(self) -> list[Node]:
        """
        Returns the list of Node objects of the graph
        """
        return list(self.nodes_dict().values())

    @property
    def edges(self) -> list[Edge]:
        """
        This method creates a list of edges from the raw edge strings. The nodes_dict is
        needed to look up the nodes by their names.
        """
        edges = []
        for i, edge in enumerate(self.edges_raw):
            edge = Edge()
            edges.append(edge.load_from_string(edge, self.nodes_dict(), i))
        return edges

    def read(self) -> Graph:
        """
        Main function of the class. It reads the file and creates a graph object.
        """
        # open file, read lines and remove comments and empty lines
        with open(f"{self.path}", "r", encoding="utf-8") as file:
            lines = []
            for line in file.readlines():
                line = line.split("#")[0].strip()
                if line != "":
                    lines.append(line)
        # retrieve number of nodes and edges and directedness
        self.node_count = int(lines.pop(0))
        self.edge_count = int(lines.pop(0))
        self.directed_raw = lines.pop(0)
        self.nodes_raw = lines[:self.node_count]
        self.edges_raw = lines[self.node_count:self.node_count + self.edge_count]
        # create graph
        return Graph(self.directed, self.nodes, self.edges)


class GraphWriter:
    """
    This class is used to create a text file from a graph object.
    """
    def __init__(self, graph: Graph, path: str, lang: str = "ger") -> None:
        self.graph = graph
        self.path = path
        self.lang = lang
        self.text = ""

    def write_blank_line(self) -> None:
        """
        Writes blank line.
        """
        self.text += "\n"

    def write_graph_info(self) -> None:
        """
        Writes the graph information to the text file.
        """
        # write graph information
        self.text += f"{self.graph.node_count}\n"
        self.text += f"{self.graph.edge_count}\n"
        if self.graph.directed:
            if self.lang == "ger":
                self.text += "gerichtet\n"
            elif self.lang == "eng":
                self.text += "directed\n"
            else:
                raise ValueError(f"Language {self.lang} not supported")
        else:
            if self.lang == "ger":
                self.text += "ungerichtet\n"
            elif self.lang == "eng":
                self.text += "undirected\n"
            else:
                raise ValueError(f"Language {self.lang} not supported")

    def write_nodes(self) -> None:
        """
        Writes the node information to the text file.
        """
        self.write_blank_line()
        if self.lang == "ger":
            self.text += "# Knotenname xKoord yKoord\n"
        elif self.lang == "eng":
            self.text += "# NodeName xCoord yCoord\n"
        else:
            raise ValueError(f"Language {self.lang} not supported")
        self.write_blank_line()
        # write nodes
        for node in self.graph.nodes:
            self.text += f"{node.name} {node.x_coord} {node.y_coord}\n"

    def write_edges(self) -> None:
        """
        Writes the edge information to the text file.
        """
        self.write_blank_line()
        if self.lang == "ger":
            self.text += "# Kantename Knotenname1 Knotenname2\n"
        elif self.lang == "eng":
            self.text += "# EdgeName NodeName1 NodeName2\n"
        else:
            raise ValueError(f"Language {self.lang} not supported")
        self.write_blank_line()
        # write edges
        for edge in self.graph.edges:
            self.text += f"{edge.name} {edge.head.name} {edge.tail.name}\n"

    def save(self) -> None:
        """
        Saves the text file.
        """
        with open(f"{self.path}/{self.graph.auto_name()}", "w", encoding="utf-8") as file:
            file.write(self.text)

    def write(self) -> None:
        """
        Writes the graph to the text file.
        """
        # write graph
        self.write_graph_info()
        self.write_nodes()
        self.write_edges()
        # save file
        self.save()
