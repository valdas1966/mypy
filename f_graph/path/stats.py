from f_cs.stats import StatsAlgo


class StatsPath(StatsAlgo):
    """
    ============================================================================
     Stats for Path-Graphs.
    ============================================================================
    """

    def __init__(self,
                  elapsed: int = 0,
                    generated: int = 0,
                      explored: int = 0) -> None:
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

    def update(self, stats: 'StatsPath') -> None:
        """
        ========================================================================
         Update the Stats.
        ========================================================================
        """
        self._elapsed += stats.elapsed
        self._generated += stats.generated
        self._explored += stats.explored
