# pylint: disable=too-many-arguments
"""
This module contains the core classes for the graph data structure. The
classes can be used to construct a graph from a file or to construct a graph
manually.
"""
from functools import lru_cache
from pathlib import Path


class Node:
    """
    Class for representing a node and its optional coordinates and weight. The class can be
    constructed with or without parameters. If no parameters are given, the load_from_string method
    can be used as an alternative constructor.
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
        self.f_edges = set()
        self.b_edges = set()

    @property
    def allowed(self) -> bool:
        """
        Returns True if the node is empty or got cleared.
        """
        return self.name is not None

    def load_from_string(self, string: str, index: int) -> None:
        """
        This method can be used as an alternative constructor. It takes a string of the format
        "name x_coord y_coord weight" and sets the corresponding parameters of the node object.
        If any of the parameters are already set, the method will raise an exception.
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
        self.f_edges = set()
        self.b_edges = set()

    def __str__(self) -> str:
        """
        Prints and returns relevant information about the node. The x and y coordinates are not
        relevant for the graph structure.
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


class Edge:
    """
    Class for representing an edge and the node indices it connects to. The class can be
    constructed with or without parameters. If no parameters are specified, the load_from_string
    method can be used as an alternative constructor.
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
        Returns True if the edge is empty or got cleared.
        """
        return self.name is not None

    def load_from_string(self, string: str, nodes_dict: dict[str, Node], index: int) -> None:
        """
        This method can be used as an alternative constructor. It takes a string of the format
        "name head_name tail_name" and sets the corresponding parameters of the edge object.
        If any of the parameters are already set, the method will raise an exception.
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
        if len(components) > 4 and not components[4].startswith("#"):
            raise Warning(
                f"Edge {''.join(components)} has additional parameters that are not yet supported!"
            )
        if len(components) < 3:
            raise ValueError(
                f"Edge: load_from_string() string {string} has incorrect format!"
            )
        # set the parameters
        self.name = components[0]
        # set head and tail nodes and index via look up in the nodes dictionary
        self.head = nodes_dict[components[1]]
        self.tail = nodes_dict[components[2]]
        # set the weight if it is given
        if len(components) == 4:
            self.weight = float(components[3])
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
        Returns relevant information about the edge if not None.
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


class Graph:
    """
    Class for a graph data structure. Translation of the graph class
    from the C++ implementation of Martin Oellrich.
    """
    def __init__(
        self,
        name: str = "",
        directed: bool = True,
        nodes: list[Node] = None,
        edges: list[Edge] = None,
        init_neighbors: bool = False,
    ):
        self.name = name
        self.directed = directed
        self.nodes = nodes
        self.edges = edges
        self.node_count = len(self.nodes) if self.nodes is not None else 0
        self.edge_count = len(self.edges) if self.edges is not None else 0
        if init_neighbors:
            self.init_neighbors()

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
        Returns the Edge object with a given name.
        """
        # TODO: this is a linear search, maybe use a dictionary instead
        for edge in self.edges:
            if edge.name == name:
                return edge
        raise ValueError(f"Graph: edge_by_name(name), Edge {name} not found!")

    def init_neighbors(self) -> None:
        """
        Searches the edges for forward and backward neighbors and stores them in the corresponding
        lists of the nodes.
        """
        for edge in self.edges:
            # add forward and backward neighbor nodes
            edge.head.f_neighbors.add(edge.tail)
            edge.tail.b_neighbors.add(edge.head)
            # add forward and backward edges
            edge.head.f_edges.add(edge)
            edge.tail.b_edges.add(edge)
        if not self.directed:
            for node in self.nodes:
                # combine forward and backward neighbor nodes
                node.f_neighbors.update(node.b_neighbors)
                node.b_neighbors = node.f_neighbors
                # combine forward and backward edges
                node.f_edges.update(node.b_edges)
                node.b_edges = node.f_edges

    def auto_name(self) -> None:
        """
        Creates a name for the graph based on the names of the nodes and edges.
        """
        if self.name == "":
            return f"graph_directed-{self.directed}_{self.node_count}-nodes_{self.edge_count}-edges"
        return self.name


class GraphReader:
    """
    Class for loading and reading the file containing the graph data.
    """
    def __init__(self, path: str, init_neighbors: bool = False) -> None:
        self.path = path
        self.node_count = None
        self.edge_count = None
        self.directed_raw = None
        self.nodes_raw = None
        self.edges_raw = None
        self.init_neighbors = init_neighbors

    @property
    def directed(self) -> bool:
        """
        Returns whether the graph is directed or not. The directedness is saved as a string
        in the file.
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
        Returns the list of Node objects of the graph.
        """
        return list(self.nodes_dict().values())

    @property
    def edges(self) -> list[Edge]:
        """
        This method creates a list of edges from the raw edge strings. The nodes_dict is needed to
        look up the nodes by their names.
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
        return Graph(
            directed=self.directed,
            nodes=self.nodes,
            edges=self.edges,
            init_neighbors=self.init_neighbors
        )


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
        # define languages and corresponding vocabulary
        vocab = {
            'ger': ('Knoten', 'Kanten', 'gerichtet', 'ungerichtet'),
            'eng': ('nodes', 'edges', 'directed', 'undirected')
        }
        # write graph information in the specified language
        for language in vocab:
            if language == self.lang:
                self.text += f"{self.graph.node_count}   # {vocab[language][0]}\n"
                self.text += f"{self.graph.edge_count}   # {vocab[language][1]}\n"
                if self.graph.directed:
                    self.text += f"{vocab[language][2]}\n"
                else:
                    self.text += f"{vocab[language][3]}\n"
                break
            raise ValueError(f"Language {self.lang} not supported")
        self.write_blank_line()

    def write_nodes(self) -> None:
        """
        Writes the node information to the text file.
        """
        # write header in the specified language
        if all(v is not None for v in [self.graph.nodes[0].x_coord, self.graph.nodes[0].y_coord]):
            if self.lang == "ger":
                self.text += "# Knotenname xKoord yKoord\n"
            elif self.lang == "eng":
                self.text += "# NodeName xCoord yCoord\n"
        elif all(v is None for v in [self.graph.nodes[0].x_coord, self.graph.nodes[0].y_coord]):
            if self.lang == "ger":
                self.text += "# Knotenname\n"
            elif self.lang == "eng":
                self.text += "# NodeName\n"
        else:
            raise ValueError(f"Language {self.lang} not supported")
        self.write_blank_line()
        # write nodes
        for node in self.graph.nodes:
            # make integers of coordinates if they are integers
            x_coord = int(node.x_coord) if node.x_coord.is_integer() else node.x_coord
            y_coord = int(node.y_coord) if node.y_coord.is_integer() else node.y_coord
            self.text += f"{node.name} {x_coord} {y_coord}\n"
        self.write_blank_line()

    def write_edges(self) -> None:
        """
        Writes the edge information to the text file.
        """
        if self.lang == "ger":
            self.text += "# Kantenname Knotenname1 Knotenname2\n"
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
        if self.path.endswith(".gra"):
            path = Path(self.path)
        elif Path(self.path).is_dir():
            path = Path(self.path) / self.graph.auto_name() / ".gra"
        elif self.path is None:
            path = Path.cwd() / self.graph.auto_name() / ".gra"
        else:
            raise ValueError(f"Path {self.path} not valid")
        with open(path, "w", encoding="utf-8") as file:
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
