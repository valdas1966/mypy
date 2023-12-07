from f_heuristic_search.algos.spp.a_star import AStar
from f_heuristic_search.problem_types.old_spp_grid import SPP
from f_heuristic_search.domain.grid.node import NodeFCell as Node


class AStarLookup(AStar):
    """
    ============================================================================
     AStar Algo with a Lookup-Table with Perfect-Heuristics
      (accurate distance to the Goal).
    ============================================================================
    """

    def __init__(self, spp: SPP, lookup: dict[Node, int] = dict()) -> None:
        AStar.__init__(self, spp=spp)
        self._lookup = lookup

    def to_lookup(self) -> dict[Node, int]:
        """
        ========================================================================
         Return a Lookup-Table (Expanded-Nodes with their G-Values - Accurate
                               distance to the Start-Node).
        ========================================================================
        """
        return {node: node.g for node in self.closed}

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Search can be terminated
          (Best=Goal or Best in the Lookup-Table).
        ========================================================================
        """
        return AStar._can_terminate(self) or self._best in self._lookup

    def _set_heuristics(self, node: Node) -> None:
        """
        ========================================================================
         Set Heuristic-Value to the Node (Perfect Heuristics if the Node is in
          the Lookup-Table or Manhattan-Distance otherwise).
        ========================================================================
        """
        if node in self._lookup:
            node.h = self._lookup[node]
        else:
            AStar._set_heuristics(self, node=node)
