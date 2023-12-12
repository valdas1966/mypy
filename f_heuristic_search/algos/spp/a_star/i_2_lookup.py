from f_heuristic_search.algos.spp.a_star.i_1_manual import AStarManual
from f_heuristic_search.algos.spp.node import Node


class AStarLookup(AStarManual):
    """
    ============================================================================
     AStar with Manual and Lookup Heuristics.
    ============================================================================
    """

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Search-Process can be Terminated.
        ========================================================================
        """
        return AStarManual._can_terminate() or self._best in self._spp.heuristics

    def _calc_heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristics-Distance from the received Node to the Goal.
        ========================================================================
        """
        if node in self._spp.heuristics:
            return self._calc_heuristics[node]
        return AStarManual._calc_heuristics(node=node)
