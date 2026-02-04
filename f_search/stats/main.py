from f_cs.stats.main import StatsAlgo


class StatsSearch(StatsAlgo):
    """
    ============================================================================
     Stats for Search-Problems.
    ============================================================================
    """

    def __init__(self,
                 elapsed: int = 0,
                 discovered: int = 0,
                 relaxed: int = 0,
                 explored: int = 0) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self, elapsed=elapsed)
        # Number of state discovered (added to the open queue)
        self._discovered = discovered
        # Number of state relaxed (updated with better priority)
        self._relaxed = relaxed
        # Number of state fully expanded (moved to closed list)
        self._explored = explored

    @property
    def discovered(self) -> int:
        """
        ========================================================================
         Return the number of discovered state.
        ========================================================================
        """
        return self._discovered

    @property
    def relaxed(self) -> int:
        """
        ========================================================================
         Return the number of relaxed state.
        ========================================================================
        """
        return self._relaxed

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the number of explored state.
        ========================================================================
        """
        return self._explored

    @discovered.setter
    def discovered(self, discovered: int) -> None:
        """
        ========================================================================
         Set the number of discovered state.
        ========================================================================
        """
        self._discovered = discovered

    @relaxed.setter
    def relaxed(self, relaxed: int) -> None:
        """
        ========================================================================
         Set the number of relaxed state.
        ========================================================================
        """
        self._relaxed = relaxed

    @explored.setter
    def explored(self, explored: int) -> None:
        """
        ========================================================================
         Set the number of explored state.
        ========================================================================
        """
        self._explored = explored
