from typing import List
from constants import NO_INDEX
from base_classes import Edge, Neighbour
from pathlib import Path


class Node:
    """
    Class for representing a node and its optional coordinates and weight. The
    class can be constructed with or without parameters. If no parameters are
    given, the load_from_string method can be used as an alternative constructor.
    """
    name: str
    x_coord: float
    y_coord: float
    weight: float
    def __init__(
            self,
            name: str = None,
            x_coord: float = None,
            y_coord: float = None,
            weight: float = None
        ):
        self.__name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.weight = weight
        
    def load_from_string(self, string: str)  -> None:
        """
        This method can be used as an alternative constructor. It takes a string
        of the format "name x_coord y_coord weight" and sets the corresponding
        parameters of the node object. If any of the parameters are already set,
        the method will raise an exception.
        """
        # check if any of the parameters are already set
        for param in [self.__name, self.x_coord, self.y_coord, self.weight]:
            if param is not None:
                raise ValueError(
                    f"Node: load_from_string()", "parameter {param} is already set!"
                )
        # split the string into its components
        components = string.split(" ")
        # check if the string has the correct format
        if len(components) != 3:
            raise ValueError(
                f"Node: load_from_string()", "string {string} has incorrect format!"
            )
        self.__name = components[0]
        self.x_coord = float(components[1])
        self.y_coord = float(components[2])
        
    @property
    def name(self) -> str:
        return self.__name

    @property
    def allowed(self) -> bool:
        """ returns whether the node got deleted or not """
        return self.__name != ""

    @property
    def __str__(self) -> str:
        """
        Prints and returns relevant information about the node. The x and y
        coordinates are not relevant for the graph structure.
        """
        out_string = self.__name
        if self.weight != None:
            out_string += f" [{self.weight}]"
        return out_string

class File:
    """
    Class for loading and reading the file containing the graph data
    """
    path: str
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
        elif self.directed_raw in ["gerichtet", "directed", "g", "G"]:
            return True
        else:
            raise ValueError(f"Directedness not specified correctly in file {self.path}")
        
    @property
    def nodes(self):
        return [Node().load_from_string(node) for node in self.nodes_raw]
    
    @property
    def edges(self):
        return [Edge(edge) for edge in self.edges_raw]
        

class Graph:
    """
    Class for a graph data structure
    translation of the graph class from the C++ implementation of Martin Oellrich
    """
    directed: bool
    filename: str
    def __init__(self, directed: bool = True, filename: str = None):
        self.__directed = directed
        self.__number_of_nodes = 0
        self.__number_of_edges = 0
        self.__nodes = []
        self.__edges = []
        self.__forward_neighbours = []
        self.__backward_neighbours = []
        # load graph from file if filename is given
        if filename is not None:
            if not isinstance(filename, str):
                raise TypeError("Graph: __init__(filename)", filename)
            if not Path(filename).is_file():
                raise FileNotFoundError("Graph: __init__(filename)", filename)
            self.load_from_file(filename)

    def load_from_file(self, filename: str):
        """ Reads the graph from a file """
        # open file, read lines and remove comments and empty lines
        with open(f"{filename}", "r") as file:
            lines = []
            for line in file.readlines():
                line = line.split("#")[0].strip()
                if line != "":
                    lines.append(line)
        # retrieve number of nodes and edges and directedness
        number_of_nodes = int(lines[0])
        number_of_edges = int(lines[1])
        if lines[2] in ["ungerichtet", "undirected", "u", "U"]:
            self.__directed = False
        # retrieve node names and coordinates
        for i in range(3, 3 + number_of_nodes):
            node_data = lines[i].split()
            self.add_node(Node(node_data[0], x_coord=float(node_data[1]), y_coord=float(node_data[2])))
        # retrieve edge data
        for i in range(3 + number_of_nodes, 3 + number_of_nodes + number_of_edges):
            edge_data = lines[i].split()
            self.add_edge(Edge(edge_data[0], self.node_index(edge_data[1]), self.node_index(edge_data[2])))

    def isdirected(self) -> bool:
        """ Returns whether the graph is directed or not """
        return self.__directed

    @property
    def nodes(self) -> List[Node]:
        """ returns the nodes array of the graph """
        return self.__nodes

    @property
    def edges(self) -> List[Edge]:
        """ returns the edges array of the graph """
        return self.__edges

    @property
    def node_count(self) -> int:
        """ returns the number of allowed nodes in the graph """
        return self.__number_of_nodes

    @property
    def edge_count(self) -> int:
        """ returns the number of allowed edges in the graph """
        return self.__number_of_edges

    # get-methods with parameters
    def node_allowed(self, i: int) -> bool:
        """ returns whether the node is allowed or not """
        return self.__nodes[i].allowed()

    def edge_allowed(self, j: int) -> bool:
        """ returns whether the edge is allowed or not """
        return self.__edges[j].allowed()

    def node(self, i: int) -> str:
        """ returns the node at the given index """
        if i >= self.node_count:
            raise IndexError("Graph: node(i)", i, self.node_count)
        if not self.node_allowed(i):
            raise ValueError("Graph: node(i), Node ", i)
        return self.__nodes[i]

    def edge(self, j: int) -> str:
        """ returns the edge at the given index """
        if j >= self.edge_count:
            raise IndexError("Graph: edge(j)", j, self.edge_count)
        if not self.edge_allowed(j):
            raise ValueError("Graph: edge(j), Edge ", j)
        return self.__edges[j]

    def node_index(self, name: str) -> int:
        """ returns the index of the node with the given name """
        for i in range(self.node_count):
            if self.__nodes[i].name == name:
                return i
        return NO_INDEX

    def edge_index(self, name: str) -> int:
        """ returns the index of the edge with the given name """
        for j in range(self.edge_count):
            if self.__edges[j].name == name:
                return j
        return NO_INDEX

    def forward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the forward neighbours of the node at the given index """
        if i >= self.node_count:
            raise IndexError("Graph: forward_neighbours(i)", i, self.edge_count)
        if not self.node_allowed(i):
            raise ValueError("Graph: forward_neighbours(i), Node ", i)
        return self.__forward_neighbours[i]

    def backward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the backward neighbours of the node at the given index """
        if i >= self.node_count:
            raise IndexError("Graph: backward_neighbours(i)", i, self.node_count)
        if not self.node_allowed(i):
            raise ValueError("Graph: backward_neighbours(i), Node ", i)
        if not self._directed():
            return self.__forward_neighbours[i]
        return self.__backward_neighbours[i]

    # for undirected graphs only
    def neighbours(self, i: int) -> List[Neighbour]:
        """ returns the neighbours of the node at the given index for undirected graphs """
        return self.forward_neighbours(i)

    def forward_extent(self, i: int) -> int:
        """ returns the number of forward neighbours of the node at the given index """
        return len(self.forward_neighbours(i))

    def backward_extent(self, i: int) -> int:
        """ returns the number of backward neighbours of the node at the given index """
        return len(self.backward_neighbours(i))

    # for undirected graphs only
    def extent(self, i: int) -> int:
        """ returns the number of neighbours of the node at the given index for undirected graphs """
        return len(self.forward_extent(i))

    def add_node(self, new_node: Node):
        """ adds a node to the graph and returns its index """
        # check if there is a deleted node, insert there if possible
        if self.node_count < len(self.__nodes):
            for i, node in enumerate(self.__nodes):
                if not node.allowed():
                    node = new_node
                    i_node = i
                    break
        else:
            self.__nodes.append(new_node)
            i_node = len(self.__nodes) - 1
            self.__forward_neighbours.append([])
            if self.isdirected is True:
                self.__backward_neighbours.append([])
        # count new node and return index
        self.__number_of_nodes += 1
        return i_node

    def add_edge(self, new_edge: Edge):
        """ adds an edge to the graph and returns its index or NO_INDEX if not possible """
        # check if there is a deleted edge, insert there if possible
        if self.edge_count < len(self.__edges):
            for j, edge in enumerate(self.__edges):
                if not edge.allowed():
                    edge = new_edge
                    j_edge = j
                    break
        else:
            self.__edges.append(new_edge)
            j_edge = len(self.__edges) - 1
        # count new edge and return index
        self.__number_of_edges += 1
        # set neighbours
        self.__forward_neighbours[new_edge.i_tail].append(Neighbour(new_edge.i_head, j_edge))
        if self.__directed is True:
            self.__backward_neighbours[new_edge.i_head].append(Neighbour(new_edge.i_tail, j_edge))
        else:
            self.__forward_neighbours[new_edge.i_head].append(Neighbour(new_edge.i_tail, j_edge))
        return j_edge

    def delete_node(self, i: int):
        """ deletes the node at the given index, returns true if successful """
        # check if node got deleted already
        if not self.node_allowed(i):
            return False
        # delete all edges connected to the node
        neighbours = self.__forward_neighbours[i].copy()
        for neighbour in neighbours:
            self.delete_edge(neighbour.j)
        # for directed graphs also delete all edges pointing towards the node
        if self.isdirected is True:
            neighbours = self.__backward_neighbours[i].copy()
            for neighbour in neighbours:
                self.delete_edge(neighbour.j)
        # overwrite with default node
        self.__nodes[i] = Node()
        # reduce node count
        self.__number_of_nodes -= 1
        return True

    def delete_edge(self, j: int):
        """ deletes the edge at the given index, returns true if successful """
        # check if edge is valid
        if not self.edge_allowed(j):
            return False
        # delete __edges[j] from __forward_neighbours
        forward_neighbours = self.__forward_neighbours[self.__edges[j].i_tail]
        for neighbour in forward_neighbours:
            if neighbour.j() == j:
                neighbour = forward_neighbours[-1]
                forward_neighbours.pop()
                break
        # delete __edges[j] from __backward_neighbours
        if self.isdirected is True:
            backward_neighbours = self.__backward_neighbours[self.__edges[j].i_head]
            for neighbour in backward_neighbours:
                if neighbour.j() == j:
                    neighbour = backward_neighbours[-1]
                    backward_neighbours.pop()
                    break
        # overwrite with default edge
        self.__edges[j] = Edge()
        # reduce edge count
        self.__number_of_edges -= 1
        return True
