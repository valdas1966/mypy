from f_cs.stats import StatsAlgo


class StatsSearch(StatsAlgo):
    """
    ============================================================================
     Stats for Search-Problems.
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
        # Number of state added to the open queue (Generated)
        self._generated = generated
        # Number of state fully expanded (moved to closed list)
        self._explored = explored

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the number of generated state.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the number of explored state.
        ========================================================================
        """
        return self._explored

    @generated.setter
    def generated(self, generated: int) -> None:
        """
        ========================================================================
         Set the number of generated state.
        ========================================================================
        """
        self._generated = generated

    @explored.setter
    def explored(self, explored: int) -> None:
        """
        ========================================================================
         Set the number of explored state.
        ========================================================================
        """
        self._explored = explored

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the stats.
        ========================================================================
        """
        return f'[Elapsed={self._elapsed}] [Generated={self._generated}] [Explored={self._explored}]'
        
