from f_cs.stats import StatsAlgo


class StatsPath(StatsAlgo):
    """
    ============================================================================
     Stats for Path-Graphs.
    ============================================================================
    """

    def __init__(self, elapsed: int, generated: int, explored: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self, elapsed=elapsed)
        self._generated: int = generated
        self._explored: int = explored

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the Number of Generated-Nodes.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the Number of Explored-Nodes.
        ========================================================================
        """
        return self._explored
