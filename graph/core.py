from typing import List
from base_classes import Neighbour
from pathlib import Path

# TODO
# - change entire structure: GraphReader --> attributes, Nodes, Edges --> Graph
#   when creating the Node objects, create hash table for the names
#   hand over Node objects to Edge objects
# - fix comments
# - add type hints
# - add logging
# - add tests
# - fix function read in class GraphReader (two functions with same name)


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
    ):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.index = index
        self.weight = weight

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
            i_head: int = None,
            i_tail: int = None,
            index: int = None,
            weight: float = None
    ):
        self.name = name
        self.i_head = i_head
        self.i_tail = i_tail
        self.index = index
        self.weight = weight

    def load_from_string(self, string: str, nodes: dict[int, Node], index: int) -> None:
        """
        This method can be used as an alternative constructor. It takes a string
        of the format "name head_name tail_name" and sets the corresponding
        parameters of the edge object. If any of the parameters are already set,
        the method will raise an exception.
        """
        # check if any of the parameters are already set
        for param in [self.name, self.i_head, self.i_tail, self.weight]:
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
        self.i_head = nodes.nodes[int(components[1])]
        self.i_tail = nodes.nodes[int(components[2])]
        self.index = index

    @property
    def allowed(self) -> bool:
        """ returns whether the edge got deleted or not """
        return self.name != ""

    def __str__(self) -> str:
        """ prints and returns relevant information about the edge """
        out_string = f"{self.name} ({self.i_head}, {self.i_tail})"
        if self.weight is not None:
            out_string += f" [{self.weight}]"
        return out_string


class GraphReader:
    """
    Class for loading and reading the file containing the graph data
    """
    def __init__(self, path: str):
        self.__path = Path(path)
        if not self.__path.is_file():
            raise FileNotFoundError("File: __init__()", self.__path)

    def read(self):
        # open file, read lines and remove comments and empty lines
        with open(f"{self.path}", "r") as file:
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

    @property
    def directed(self):
        if self.directed_raw in ["ungerichtet", "undirected", "u", "U"]:
            return False
        if self.directed_raw in ["gerichtet", "directed", "g", "G"]:
            return True
        raise ValueError(f"Directedness not specified correctly in file {self.path}")

    @property
    def nodes(self):
        return [Node().load_from_string(node, i) for i, node in enumerate(self.nodes_raw)]

    @property
    def edges(self):
        edges = []
        for i, edge in enumerate(self.edges_raw):
            edges.append(Edge().load_from_string(edge, self.nodes_dict), i)
        return edges
    
    def read(self):
        """
        Method for instantiating the Graph class from a file
        """
        return Graph(self.directed, self.nodes, self.edges)


class Graph:
    """
    Class for a graph data structure
    translation of the graph class from the C++ implementation of Martin Oellrich
    """
    def __init__(
        self, directed: bool = True,
        nodes: list[Node] = None,
        edges: list[Edge] = None
    ):
        self.directed = directed
        self.nodes = nodes
        self.edges = edges
        self.node_count = len(self.nodes)
        self.edge_count = len(self.edges)
        self.forward_neighbours = []
        self.backward_neighbours = []

    def node_by_name(self, name: str) -> Node:
        for node in self.nodes:
            if node.name == name:
                return node
        raise ValueError(f"Graph: node_by_name(name), Node {name} not found!")

    def edge_by_name(self, name: str) -> Edge:
        for edge in self.edges:
            if edge.name == name:
                return edge
        raise ValueError(f"Graph: edge_by_name(name), Edge {name} not found!")

    def get_forward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the forward neighbours of the node at the given index """
        if i >= self.node_count:
            raise IndexError("Graph: get_forward_neighbours(i)", i, self.edge_count)
        if not self.nodes[i].allowed:
            raise ValueError("Graph: get_forward_neighbours(i), Node ", i)
        return self.forward_neighbours[i]

    def get_backward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the backward neighbours of the node at the given index """
        if i >= self.node_count:
            raise IndexError("Graph: get_backward_neighbours(i)", i, self.node_count)
        if not self.nodes[i].allowed:
            raise ValueError("Graph: get_backward_neighbours(i), Node ", i)
        if not self.directed:
            return self.forward_neighbours[i]
        return self.backward_neighbours[i]

    # for undirected graphs only
    def neighbours(self, i: int) -> List[Neighbour]:
        """ returns the neighbours of the node at the given index for undirected graphs """
        return self.get_forward_neighbours(i)

    def forward_extent(self, i: int) -> int:
        """ returns the number of forward neighbours of the node at the given index """
        return len(self.get_forward_neighbours(i))

    def backward_extent(self, i: int) -> int:
        """ returns the number of backward neighbours of the node at the given index """
        return len(self.get_backward_neighbours(i))

    # for undirected graphs only
    def extent(self, i: int) -> int:
        """ returns the number of neighbours of the node at the given index """
        return len(self.forward_extent(i))

    def add_node(self, new_node: Node):
        """ adds a node to the graph and returns its index """
        # check if there is a deleted node, insert there if possible
        if self.node_count < len(self.nodes):
            for i, node in enumerate(self.nodes):
                if not node.allowed():
                    node = new_node
                    i_node = i
                    break
        else:
            self.nodes.append(new_node)
            i_node = len(self.nodes) - 1
            self.forward_neighbours.append([])
            if self.directed is True:
                self.backward_neighbours.append([])
        # count new node and return index
        self.node_count += 1
        return i_node

    def add_edge(self, new_edge: Edge):
        """ adds an edge to the graph and returns its index or NO_INDEX if not possible """
        # check if there is a deleted edge, insert there if possible
        if self.edge_count < len(self.edges):
            for j, edge in enumerate(self.edges):
                if not edge.allowed():
                    edge = new_edge
                    j_edge = j
                    break
        else:
            self.edges.append(new_edge)
            j_edge = len(self.edges) - 1
        # count new edge and return index
        self.edge_count += 1
        # set neighbours
        self.forward_neighbours[new_edge.i_tail].append(Neighbour(new_edge.i_head, j_edge))
        if self.directed is True:
            self.backward_neighbours[new_edge.i_head].append(Neighbour(new_edge.i_tail, j_edge))
        else:
            self.forward_neighbours[new_edge.i_head].append(Neighbour(new_edge.i_tail, j_edge))
        return j_edge

    def delete_node(self, i: int):
        """ deletes the node at the given index, returns true if successful """
        # check if node got deleted already
        if not self.nodes[i].allowed:
            return False
        # delete all edges connected to the node
        neighbours = self.forward_neighbours[i].copy()
        for neighbour in neighbours:
            self.delete_edge(neighbour.j)
        # for directed graphs also delete all edges pointing towards the node
        if self.directed is True:
            neighbours = self.backward_neighbours[i].copy()
            for neighbour in neighbours:
                self.delete_edge(neighbour.j)
        # overwrite with default node
        self.nodes[i] = Node()
        # reduce node count
        self.node_count -= 1
        return True

    def delete_edge(self, j: int):
        """ deletes the edge at the given index, returns true if successful """
        # check if edge is valid
        if not self.edges[j].allowed:
            return False
        # delete edges[j] from forward_neighbours
        forward_neighbours = self.forward_neighbours[self.edges[j].i_tail]
        for neighbour in forward_neighbours:
            if neighbour.j() == j:
                neighbour = forward_neighbours[-1]
                forward_neighbours.pop()
                break
        # delete edges[j] from backward_neighbours
        if self.directed is True:
            backward_neighbours = self.backward_neighbours[self.edges[j].i_head]
            for neighbour in backward_neighbours:
                if neighbour.j() == j:
                    neighbour = backward_neighbours[-1]
                    backward_neighbours.pop()
                    break
        # overwrite with default edge
        self.edges[j] = Edge()
        # reduce edge count
        self.edge_count -= 1
        return True
