from f_heuristic_search.algos.mixins.spp import SPPAlgo
from f_heuristic_search.problem_types.spp_grid import SPP
from f_heuristic_search.nodes.i_2_f import NodeF as Node


class AStar(SPPAlgo):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        SPPAlgo.__init__(self, spp)

    def run(self) -> None:
        """
        ========================================================================
         Executes the Algorithm.
        ========================================================================
        """
        self.open.push(self.spp.start)
        while len(self.open):
            best = self.open.pop()
            self.closed.push(best)
            if self._can_terminate(node=best):
                self._is_path_found = True
                return
            self._expand_node(best)
        # Path not found
        self._is_path_found = False

    def _expand_node(self, node: Node) -> None:
        """
        ========================================================================
         Visits the Node and Generates its Children.
        ========================================================================
        """
        for child in self.spp.graph.get_neighbors(node):
            if self._is_expanded(child):
                continue
            if self._is_generated(child):
                self._try_new_parent(child=child, parent=node)
            else:
                self._generate_node(child)

    def _try_new_parent(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Set a new Parent to a Child if the path from the Start to it is
          nearer (less G-Value).
        ========================================================================
        """
        node = self.open.get(child)
        if node.is_better_parent(parent):
            node.parent = parent
