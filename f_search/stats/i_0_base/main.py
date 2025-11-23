from f_cs.stats import StatsAlgo


class StatsSearch(StatsAlgo):
    """
    ============================================================================
     Stats for Search-Problems.
    ============================================================================
    """

    def __init__(self, name: str = 'StatsSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self, name=name)
        self.generated = 0
        self.explored = 0

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the Stats.
        ========================================================================
        """
        return f'Stats(generated={self.generated}, explored={self.explored})'