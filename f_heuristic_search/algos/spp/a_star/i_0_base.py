from f_heuristic_search.algos.spp.base import SPPAlgo, Node
from abc import ABC, abstractmethod


class AStarBase(ABC, SPPAlgo[Node]):
    """
    ============================================================================
     Base-Class for A* Algorithm.
    ============================================================================
    """

    def run(self) -> None:
        """
        ========================================================================
         Executes the Algorithm.
        ========================================================================
        """
        self._generate_node(self.spp.start)
        while len(self.open):
            self._best = self.open.pop()
            self.closed.add(self._best)
            if self._can_terminate():
                self._is_path_found = True
                return
            self._expand_best()
        # Path not found
        self._is_path_found = False

    def _expand_best(self) -> None:
        """
        ========================================================================
         Generates Best-Node Children.
        ========================================================================
        """
        for child in self.spp.graph.get_neighbors(self._best):
            if self._is_expanded(child):
                continue
            if self._is_generated(child):
                child.update_parent_if_needed(parent=self._best)
            else:
                self._generate_node(child)

    def _generate_node(self, node: Node) -> None:
        """
        ========================================================================
         Generate Best-Node's Child.
         Update Node's Parent, Set a Heuristic-Value and Push it into the Open.
        ========================================================================
        """
        if self._best:
            node.update_parent(parent=self._best)
        node.h = self._calc_heuristics(node)
        self.open.push(node)

    @abstractmethod
    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Search-Process can be Terminated.
        ========================================================================
        """
        pass

    @abstractmethod
    def _calc_heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristics-Distance from the received Node to the Goal.
        ========================================================================
        """
        pass
