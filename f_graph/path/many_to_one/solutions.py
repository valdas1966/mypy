from f_graph.path.solutions import SolutionsPath, Solution, Node


class SolutionsManyToOne(SolutionsPath):
    """
    ============================================================================
     Solutions for Many-To-One Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 sols: dict[Node, Solution],
                 changed: dict[int, int] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionsPath.__init__(self, is_valid=is_valid, sols=sols)
        self._changed: dict[int, int] = changed if changed else dict()

    @property
    def changed(self) -> dict[int, int]:
        """
        ========================================================================
         Return the Number of Changed-Nodes.
        ========================================================================
        """
        return self._changed
