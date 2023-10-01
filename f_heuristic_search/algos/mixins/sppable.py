from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.nodes.node_1_cell import NodeCell


class SPPAble:
    """
    ============================================================================
     Mixin designed for algorithms that solve Shortest Path Problems.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. optimal_path() -> list[NodeCell]
           [*] Returns an Optimal-Path from Start to Goal
               (an empty list is returned if the Goal is unreachable).
    ============================================================================
    """

    spp: SPP                    # Shortest Path Problem
    is_path_found: bool         # True if found a path from Start to Goal

    def __init__(self, spp: SPP) -> None:
        self._spp = spp
        self._is_path_found = None

    @property
    def spp(self) -> SPP:
        return self._spp

    @property
    def is_path_found(self) -> bool:
        return self._is_path_found

    def optimal_path(self) -> list[NodeCell]:
        """
        ========================================================================
         Returns an Optimal-Path from Start to Goal (empty list if unreachable).
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        return self.spp.goal.path_from(self.spp.start)
