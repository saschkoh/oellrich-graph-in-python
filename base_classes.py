""" Base classes for the graph data structure """

from constants import NO_INDEX, UNUSED






class Neighbour:
    """ class to store the indices of a neighbour node and connecting edge """
    def __init__(self, i_node: int = NO_INDEX, j_edge: int = NO_INDEX):
        self.__i_node = i_node
        self.__j_edge = j_edge

    @property
    def i(self) -> int:
        """ returns the index of the node """
        return self.__i_node

    @property
    def j(self) -> int:
        """ returns the index of the edge """
    
    @property
    def __str__(self) -> str:
        pass
