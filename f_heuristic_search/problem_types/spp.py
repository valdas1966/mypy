from f_heuristic_search.nodes.i_1_g import NodeG
from f_data_structure.graphs.abc.base import GraphBase
from typing import Generic, TypeVar
Node = TypeVar('Node', bound=NodeG)
Graph = TypeVar('Graph', bound=GraphBase)


class SPP(Generic[Graph, Node]):
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._graph = graph
        self._start = start
        self._goal = goal

    @property
    # SPP Start-Node
    def start(self) -> Node:
        return self._start

    @property
    # SPP Goal-Node
    def goal(self) -> Node:
        return self._goal

    @property
    # SPP Graph
    def graph(self) -> Graph:
        return self._graph

    def __str__(self) -> str:
        return f'SPP[{self._graph.name}]: {self._start} -> {self._goal}'

    def __repr__(self) -> str:
        return self.__str__()
