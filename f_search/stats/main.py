from f_cs.stats import StatsAlgo


class StatsSearch(StatsAlgo):
    """
    ============================================================================
     Stats for Search-Problems.
    ============================================================================
    """

    RECORD_SPEC = {'generated': lambda o: o.generated,
                   'explored': lambda o: o.explored}

    def __init__(self,
                 generated: int = 0,
                 explored: int = 0) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self)
        # Number of states added to the open queue (Generated)
        self._generated = generated
        # Number of states fully expanded (moved to closed list)
        self._explored = explored

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the number of generated states.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the number of explored states.
        ========================================================================
        """
        return self._explored

    @generated.setter
    def generated(self, generated: int) -> None:
        """
        ========================================================================
         Set the number of generated states.
        ========================================================================
        """
        self._generated = generated

    @explored.setter
    def explored(self, explored: int) -> None:
        """
        ========================================================================
         Set the number of explored states.
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
        
