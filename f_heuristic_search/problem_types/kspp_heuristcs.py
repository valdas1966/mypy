from f_heuristic_search.problem_types.kspp import KSPP, Graph
from f_heuristic_search.nodes.i_2_f import NodeF as Node
from typing import Callable


class KSPPHeuristics(KSPP):
    """
    ============================================================================
     Represents K-Shortest-Path-Problems with Heuristics.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: list[Node],
                 heuristics: Callable) -> None:
        KSPP.__init__(self, graph, start, goals)
        self._heuristics = heuristics
