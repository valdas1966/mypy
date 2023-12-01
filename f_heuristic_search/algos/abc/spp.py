from f_heuristic_search.algos.mixins.has_open_closed import HasOpenClosed
from f_heuristic_search.problem_types.spp_grid import SPP
from f_heuristic_search.nodes.i_2_f_cell import NodeFCell as Node
from abc import ABC


class SPPAlgo(ABC, HasOpenClosed):
    """
    ============================================================================
     Mixin designed for algorithms that solve Shortest Path Problems.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        HasOpenClosed.__init__(self)
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
        return self.spp.goal.path_from_root()

    def _generate_node(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Set a Heuristic-Value to the Node and Push it into the Open.
        ========================================================================
        """
        if parent:
            node.parent = parent
            node.update_g()
        node.h = node.distance(self.spp.goal)
        self.open.push(node)

    def _can_terminate(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Search can be terminated (the Goal is found).
        ========================================================================
        """
        return node == self.spp.goal
