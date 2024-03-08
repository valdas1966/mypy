from typing import Type
from f_heuristic_search.nodes.i_1_g import NodeG as Node
from f_data_structure.graphs.abc.base import GraphBase as Graph
"""
from typing import Generic, TypeVar
Node = TypeVar('Node', bound=NodeG)
Graph = TypeVar('Graph', bound=GraphBase)
"""


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 graph: Type[Graph],
                 start: Type[Node],
                 goal: Type[Node],
                 heuristics: dict[Type[Node], int] = dict()) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._graph = graph
        self._start = start
        self._goal = goal
        self._heuristics = heuristics

    @property
    # SPP Start-Node
    def start(self) -> Type[Node]:
        return self._start

    @property
    # SPP Goal-Node
    def goal(self) -> Type[Node]:
        return self._goal

    @property
    # SPP Graph
    def graph(self) -> Type[Graph]:
        return self._graph

    @property
    # Heuristic-Distance from Node to Goal
    def heuristics(self) -> dict[Type[Node], int]:
        return self._heuristics

    def __str__(self) -> str:
        return f'SPP[{self._graph.name}]: {self._start} -> {self._goal}'

    def __repr__(self) -> str:
        return self.__str__()
