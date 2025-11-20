from f_cs.stats import StatsAlgo


class StatsSearch(StatsAlgo):
    """
    ============================================================================
     Stats for Search-Problems.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatsAlgo.__init__(self)
        self.generated = 0
        self.explored = 0
