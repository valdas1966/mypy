from f_heuristic_search.nodes.i_1_g import NodeG as Node
from f_data_structure.graphs.abc.base import GraphBase as Graph


class KSPP:
    """
    ============================================================================
     Represents K-Shortest-Path-Problems with the same Start.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: tuple[Node]) -> None:
        self._graph = graph
        self._start = start
        self._goals = goals

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def start(self) -> Node:
        return self._start

    @property
    def goals(self) -> tuple[Node]:
        return self._goals
