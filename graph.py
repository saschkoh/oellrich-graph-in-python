from typing import List
from constants import NO_INDEX
from base_classes import Node, Edge, Neighbour


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

        if filename:
            self._load(filename)

    def _load(self, filename: str):
        """ reads the graph from a file """
        pass

    @property
    def isdirected(self) -> bool:
        """ returns whether the graph is directed or not """
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
        if i >= self.__number_of_nodes:
            raise IndexError("Graph: node(i)", i, self.__number_of_nodes)
        if not self.node_allowed(i):
            raise ValueError("Graph: node(i), Node ", i)
        return self.__nodes[i]

    def edge(self, j: int) -> str:
        """ returns the edge at the given index """
        if j >= self.__number_of_edges:
            raise IndexError("Graph: edge(j)", j, self.__number_of_edges)
        if not self.edge_allowed(j):
            raise ValueError("Graph: edge(j), Edge ", j)
        return self.__edges[j]

    def node_index(self, name: str) -> int:
        """ returns the index of the node with the given name """
        for i in range(self.__number_of_nodes):
            if self.__nodes[i].name() == name:
                return i
        return NO_INDEX

    def edge_index(self, name: str) -> int:
        """ returns the index of the edge with the given name """
        for j in range(self.__number_of_edges):
            if self.__edges[j].name() == name:
                return j
        return NO_INDEX

    def forward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the forward neighbours of the node at the given index """
        if i >= self.__number_of_nodes:
            raise IndexError("Graph: forward_neighbours(i)", i, self.__number_of_nodes)
        if not self.node_allowed(i):
            raise ValueError("Graph: forward_neighbours(i), Node ", i)
        return self.__forward_neighbours[i]

    def backward_neighbours(self, i: int) -> List[Neighbour]:
        """ returns the backward neighbours of the node at the given index """
        if i >= self.__number_of_nodes:
            raise IndexError("Graph: backward_neighbours(i)", i, self.__number_of_nodes)
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
        if self.__number_of_nodes < len(self.__nodes):
            for i, node in enumerate(self.__nodes):
                if not node.allowed():
                    node = new_node
                    i_node = i
                    break
        else:
            self.__nodes.append(new_node)
            i_node = len(self.__nodes) - 1
            self.__forward_neighbours.append([])
            if self._directed is True:
                self.__backward_neighbours.append([])
        # count new node and return index
        self.__number_of_nodes += 1
        return i_node

    def add_edge(self, new_edge: Edge):
        """ adds an edge to the graph and returns its index or NO_INDEX if not possible """
        # check if there is a deleted edge, insert there if possible
        if self.__number_of_edges < len(self.__edges):
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
        self.__forward_neighbours[new_edge.i_tail()].append(Neighbour(new_edge.i_head(), j_edge))
        if self.__directed is True:
            self.__backward_neighbours[new_edge.i_head()].append(Neighbour(new_edge.i_tail(), j_edge))
        else:
            self.__forward_neighbours[new_edge.i_head()].append(Neighbour(new_edge.i_tail(), j_edge))
        return j_edge

    def delete_node(self, i: int):
        """ deletes the node at the given index, returns true if successful """
        # check if node got deleted already
        if not self.node_allowed(i):
            return False
        # delete all edges connected to the node
        neighbours = self.__forward_neighbours[i].copy()
        for neighbour in neighbours:
            self.delete_edge(neighbour.j())
        # for directed graphs also delete all edges pointing towards the node
        if self.__directed is True:
            neighbours = self.__backward_neighbours[i].copy()
            for neighbour in neighbours:
                self.delete_edge(neighbour.j())
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
        forward_neighbours = self.__forward_neighbours[self.__edges[j].i_tail()]
        for neighbour in forward_neighbours:
            if neighbour.j() == j:
                neighbour = forward_neighbours[-1]
                forward_neighbours.pop()
                break
        # delete __edges[j] from __backward_neighbours
        if self.__directed is True:
            backward_neighbours = self.__backward_neighbours[self.__edges[j].i_head()]
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
