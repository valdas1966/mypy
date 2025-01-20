from f_cs.stats import StatsAlgo


class StatsPath(StatsAlgo):
    """
    ============================================================================
     Stats for Path-Graphs.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self)
        self._explored: int = None

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the Number of Explored-Nodes.
        ========================================================================
        """
        return self._explored
