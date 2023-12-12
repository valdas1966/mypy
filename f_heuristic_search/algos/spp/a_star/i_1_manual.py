from f_heuristic_search.algos.spp.a_star.i_0_base import AStarBase
from f_heuristic_search.algos.spp.node import Node


class AStarManual(AStarBase):
    """
    ============================================================================
     AStar with Manual-Heuristics.
    ============================================================================
    """

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Search-Process can be Terminated.
        ========================================================================
        """
        return self._best == self._spp.goal

    def _calc_heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristics-Distance from the received Node to the Goal.
        ========================================================================
        """
        return self._spp.heuristics[node]

