""" base classes for the graph data structure """

from constants import NO_INDEX, UNUSED


class Node:
    """ class to represent a node and its optional coordinates and weight """
    def __init__(self, name: str, x_coord: float = UNUSED, y_coord: float = UNUSED, weight: float = UNUSED):
        self.__name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.weight = weight

    def name(self) -> str:
        """ returns the name of the node """
        return self.__name

    def allowed(self) -> bool:
        """ returns whether the node got deleted or not """
        return bool(self.__name and self.__name.strip())

    def __str__(self) -> str:
        """ prints and returns relevant information about the node """
        """ the x and y coordinates are not relevant for the graph structure """
        out_string = self.__name
        if self.weight != UNUSED:
            out_string += f" [{self.weight}]"
        # print(out_string)
        return out_string


class Edge:
    """ class to represent an edge and the node indices it connects """
    def __init__(self, name: str, i_head: int, i_tail: int, weight: float = UNUSED):
        self.__name = name
        self.__i_head = i_head
        self.__i_tail = i_tail
        self.weight = weight

    def name(self) -> str:
        """ returns the name of the edge """
        return self.__name

    def i_tail(self) -> int:
        """ returns the index of the tail node """
        return self.__i_tail

    def i_head(self) -> int:
        """ returns the index of the head node """
        return self.__i_head

    def allowed(self) -> bool:
        """ returns whether the edge got deleted or not """
        return bool(self.__name and self.__name.strip())

    def __str__(self) -> str:
        """ prints and returns relevant information about the edge """
        out_string = f"{self.__name} ({self.__i_head}, {self.__i_tail})"
        if self.weight != UNUSED:
            out_string += f" [{self.weight}]"
        # print(out_string)
        return out_string


class Neighbour:
    """ class to store the indices of a neighbour node and connecting edge """
    def __init__(self, i_node: int = NO_INDEX, j_edge: int = NO_INDEX):
        self.__i_node = i_node
        self.__j_edge = j_edge

    def i(self) -> int:
        """ returns the index of the node """
        return self.__i_node

    def j(self) -> int:
        """ returns the index of the edge """
        return self.__j_edge
