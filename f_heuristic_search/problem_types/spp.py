from f_heuristic_search.nodes.i_2_f import NodeF as Node
from f_data_structure.graphs.abc.base import GraphBase as Graph
from typing import Type


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 graph: Type[Graph],
                 start: Type[Node],
                 goal: Type[Node]) -> None:
        self._graph = graph
        self._start = start
        self._goal = goal

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

    def __str__(self) -> str:
        return f'SPP[{self._graph.name}]: {self._start} -> {self._goal}'

    def __repr__(self) -> str:
        return self.__str__()
