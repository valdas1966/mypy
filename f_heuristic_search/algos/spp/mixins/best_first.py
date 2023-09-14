from typing import Type
from f_heuristic_search.algos.spp.mixins.open_closed import OpenClosed
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.nodes.node_1_cell import NodeCell


class BestFirst(OpenClosed):
    """
    ============================================================================
     Mixin for Best-First Search Algorithms.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. spp (SPP)                : Shortest Path Problem (Grid, Start, Goal).
        2. is_path_found (bool)     : True if there is path from Start to Goal.
        3. open (Priority Queue)    : Generated Nodes (not expanded yet).
        4. closed (set[NodeBase])   : Expanded Nodes.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
           [*] Executes the Algorithm.
    ============================================================================
    """

    def __init__(self,
                 spp: SPP,
                 node: Type[NodeCell] = NodeCell) -> None:
        OpenClosed.__init__(self)
        self._spp = spp
        self._start = node(cell=spp.start)
        self._goal = node(cell=spp.goal)
        self._is_path_found = None

    def run(self) -> None:
        """
        ========================================================================
         Executes the Algorithm.
        ------------------------------------------------------------------------
            1. Inits the Open with the Start-Node.
            2. While Open is not empty:
                2.1 Pop the Best-Node of Open.
                2.2 If the Best is the Goal:
                    2.2.1 Terminate the Search.
                2.3 Else:
                    2.2.2 Expand(Best).
            3. Path from Start to Goal was not found.
        ========================================================================
        """
        self.open.push(self._start)
        while self.open:
            best = self.open.pop()
            if best == self._goal:
                self._is_path_found = True
                return
            self._expand_node(node=best)
        self._is_path_found = False

    def _expand_node(self, node: NodeCell) -> None:
        """
        ========================================================================
         1. Push Node's Children into the Open if they are not in Open|Closed.
         2. Updates Child's Parent if the new is better (with lowest G-Value).
        ========================================================================
        """
        for child in node.children():
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
         Returns Heuristic-Distance between the received Node and the Goal.
        ========================================================================
        """
        return node.distance(self._goal)
