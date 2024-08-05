from f_heuristic_search.algos.spp.i_1_astar import AStar, Node
from f_heuristic_search.problem_types.spp.i_2_lookup import SPPLookup
from typing import Generic, TypeVar

SPP = TypeVar('SPP', bound=SPPLookup)


class AStarLookup(Generic[SPP, Node], AStar[SPP, Node]):
    """
    ============================================================================
     1. AStar Algo with list Lookup-Table.
     2. The Lookup-Table maps Nodes to their Optimal-Path to Goal.
    ============================================================================
    """

    def __str__(self, spp: SPP) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AStar.__init__(self, spp=spp)

    def path_optimal(self) -> list[Node]:
        """
        ========================================================================
         Return the Optimal-Path from Start to Goal.
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        if self._best == self.spp.goal:
            return AStar.path_optimal(self)
        # From Start to Best
        path = self._best.path_from_root()
        # From Best to Goal
        path.extend(self.spp.lookup[self._best])
        return path

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Node is Goal or if it is in list Lookup-Table
          (because now we now the Optimal-Path to the Goal).
        ========================================================================
        """
        return AStar._can_terminate(self) or self._best in self.spp.lookup
