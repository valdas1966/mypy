from f_heuristic_search.nodes.i_3_f_cell import NodeFCell as Node


class HasGoal:
    """
    ============================================================================
     Mixin-Class for Problems with a Goal Node.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        self._goal = goal

    @property
    def goal(self) -> Node:
        return self._goal
