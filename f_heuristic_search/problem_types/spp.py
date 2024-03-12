from f_heuristic_search.nodes.i_1_g import NodeG as Node
from f_data_structure.graphs.abc.base import GraphBase as Graph


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 heuristics: dict[Node, int] = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._graph = graph
        self._start = start
        self._goal = goal
        self._heuristics = heuristics or dict()

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

    def heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return the Heuristic-Distance from the given Node to the Goal.
        ========================================================================
        """
        return self._heuristics[node]

    def __str__(self) -> str:
        return f'SPP[{self._graph.name}]: {self._start} -> {self._goal}'

    def __repr__(self) -> str:
        return self.__str__()
