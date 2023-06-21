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
# - modify GraphWriter class to sort nodes by index


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
        self.f_neighbors = set()
        self.b_neighbors = set()

    @property
    def allowed(self) -> bool:
        """ returns whether the node got deleted or not """
        return self.name is not None

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
        if len(components) not in [1, 3]:
            raise ValueError(
                f"Node: load_from_string() string {string} has incorrect format!"
            )
        self.name = components[0]
        if len(components) == 3:
            self.x_coord = float(components[1])
            self.y_coord = float(components[2])
        self.index = index

    def clear(self) -> None:
        """
        Clears the node attributes except for the index.
        """
        self.name = None
        self.x_coord = None
        self.y_coord = None
        self.weight = None
        self.f_neighbors = set()
        self.b_neighbors = set()

    def __str__(self) -> str:
        """
        Prints and returns relevant information about the node. The x and y
        coordinates are not relevant for the graph structure.
        """
        out_string = "Object type: Node"
        if self.name is not None:
            out_string += f", name: {self.name}"
        if self.x_coord is not None:
            out_string += f", x_coord: {self.x_coord}"
        if self.y_coord is not None:
            out_string += f", y_coord: {self.y_coord}"
        if self.index is not None:
            out_string += f", index: {self.index}"
        if self.weight is not None:
            out_string += f", weight: {self.weight}"
        return out_string

    def __eq__(self, __value: object) -> bool:
        """
        Two nodes are equal if all their attributes are equal.
        """
        if isinstance(__value, Node):
            if all([
                self.name == __value.name,
                self.x_coord == __value.x_coord,
                self.y_coord == __value.y_coord,
                self.index == __value.index,
                self.weight == __value.weight
            ]):
                return True
        else:
            raise TypeError("Can only compare two Node objects!")
        return False


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

    @property
    def allowed(self) -> bool:
        """
        returns whether the edge got deleted or not
        """
        return self.name is not None

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

    def clear(self) -> None:
        """
        Clears the edge attributes except for the index.
        """
        self.name = None
        self.head = None
        self.tail = None
        self.weight = None

    def __str__(self) -> str:
        """
        prints and returns relevant information about the edge
        """
        out_string = "Object type: Edge"
        if self.name is not None:
            out_string += f", name: {self.name}"
        if self.head is not None:
            out_string += f", head: {self.head.name}"
        if self.tail is not None:
            out_string += f", tail: {self.tail.name}"
        if self.index is not None:
            out_string += f", index: {self.index}"
        if self.weight is not None:
            out_string += f", weight: {self.weight}"
        return out_string

    def __eq__(self, __value: object) -> bool:
        """
        Two edges are equal if all their attributes are equal.
        """
        if isinstance(__value, Edge):
            if all([
                self.name == __value.name,
                self.head == __value.head,
                self.tail == __value.tail,
                self.index == __value.index,
                self.weight == __value.weight
            ]):
                return True
        else:
            raise TypeError("Can only compare two Edge objects!")
        return False


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
        self.node_count = len(self.nodes) if self.nodes is not None else 0
        self.edge_count = len(self.edges) if self.edges is not None else 0

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
            edge.head.f_neighbors.add(edge.tail)
            edge.tail.b_neighbors.add(edge.head)
        if not self.directed:
            for node in self.nodes:
                # combine forward and backward neighbors
                node.f_neighbors.update(node.b_neighbors)
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
        for i, edge_raw in enumerate(self.edges_raw):
            edge = Edge()
            edge.load_from_string(edge_raw, self.nodes_dict(), i)
            edges.append(edge)
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
        return Graph(directed=self.directed, nodes=self.nodes, edges=self.edges)


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
        self.write_blank_line()

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
