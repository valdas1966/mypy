from f_heuristic_search.problem_types.spp_grid import SPP
from f_heuristic_search.nodes.i_2_f import NodeF as Node


class SPPAble:
    """
    ============================================================================
     Mixin designed for algorithms that solve Shortest Path Problems.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        self._spp = spp
        self._is_path_found = None

    @property
    # Shortest Path Problem
    def spp(self) -> SPP:
        return self._spp

    @property
    # True if found a path from Start to Goal
    def is_path_found(self) -> bool:
        return self._is_path_found

    def optimal_path(self) -> list[Node]:
        """
        ========================================================================
         Returns an Optimal-Path from Start to Goal (empty list if unreachable).
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        return self.spp.goal.path_from(self.spp.start)
