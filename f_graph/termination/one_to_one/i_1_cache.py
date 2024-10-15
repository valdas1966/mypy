from f_graph.termination.one_to_one.i_0_goal import TerminationGoal, Node


class TerminationCache(TerminationGoal):
    """
    ============================================================================
     Termination of Search-Algo with single Goal and Cache of Nodes with
     known optimal paths to Goal.
    ============================================================================
    """

    def __init__(self, goal: Node, cache: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        TerminationGoal.__init__(self, goal=goal)
        self._cache = cache

    def can(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node is a Goal or is in the Cache.
        ========================================================================
        """
        return TerminationGoal.can(self, node=node) or node in self._cache
