from f_heuristic_search.algos.mixins.has_open_closed import HasOpenClosed
from f_heuristic_search.algos.mixins.sppable import SPPAble
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.nodes.node_1_cell import NodeCell
from f_data_structure.priority_queue import PriorityQueue


class BestFirst(SPPAble, HasOpenClosed):
    """
    ============================================================================
     Mixin for Best-First Search Algorithms.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
           [*] Executes the Algorithm.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. optimal_path() -> list[NodeCell]
           [*] Returns an Optimal-Path from Start to Node.
               An empty list is returned if the Goal is unreachable.
    ============================================================================
    """

    spp: SPP                       # Shortest Path Problem
    is_path_found: bool            # True if found a path from Start to Goal
    open: PriorityQueue[NodeCell]  # Queue of generated nodes (not expanded yet)
    closed: set[NodeCell]          # Set of expanded (visited) nodes

    def __init__(self, spp: SPP) -> None:
        SPPAble.__init__(self, spp)
        HasOpenClosed.__init__(self)

    def run(self) -> None:
        """
        ========================================================================
         Executes the Algorithm.
        ========================================================================
        """
        self.open.push(self.spp.start)
        while self.open:
            best = self.open.pop()
            if best == self.spp.goal:
                self._is_path_found = True
                return
            self._expand_node(node=best)
        self._is_path_found = False

    def _expand_node(self, node: NodeCell) -> None:
        """
        ========================================================================
         1. Push Node's Children into the Open if they are not in Open|Closed.
         2. Updates a child's parent if the new parent is better
             (offers a lower G-value).
        ========================================================================
        """
        for child in self.spp.grid.neighbors(node):
            if child in self.closed:
                continue
            if child not in self.open:
                child.h = self.h_to_goal(child)
                self.open.push(child)
            elif child.is_better_parent(node):
                child.parent = node
        self.closed.add(node)

    def h_to_goal(self, node: NodeCell) -> int:
        """
        ========================================================================
         Returns Heuristic-Distance between the given Node and the Goal.
        ========================================================================
        """
        return node.distance(self.spp.goal)
