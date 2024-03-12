from f_heuristic_search.problem_types.kspp.i_0_concrete import KSPP, Graph
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
                 goals: tuple[Node],
                 heuristics: Callable[[Node, tuple[Node, ...]], int]) -> None:
        KSPP.__init__(self, graph, start, goals)
        self._heuristics = heuristics

    def heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from Node to Goals.
        ========================================================================
        """
        return self._heuristics(node, self.goals)
