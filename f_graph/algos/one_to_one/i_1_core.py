from f_graph.algos.one_to_one.i_0_abc import AlgoOneToOneABC, Problem, Node


class AlgoOneToOneCore(AlgoOneToOneABC[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def _can_terminate(self, best: Node) -> bool:
        """
        ========================================================================
         Terminate the Search if the Best-Generated-Node is a Goal.
        ========================================================================
        """
        return best == self._problem.goal

    def _construct_path(self, best: Node) -> None:
        """
        ========================================================================
         Construct an Optimal-Path from Start to the Best-Node (the Goal).
        ========================================================================
        """
        self._path = best.path_from_start()
