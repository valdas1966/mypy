from f_heuristic_search.nodes.i_2_f import NodeF as Node
from f_data_structure.graphs.i_0_base import GraphBase as Graph


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 start: Node,
                 goal: Node,
                 graph: Graph) -> None:
        start.name = 'START'
        goal.name = 'GOAL'
        self._start = start
        self._goal = goal
        self._graph = graph

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
