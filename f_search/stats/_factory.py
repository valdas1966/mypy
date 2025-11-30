from f_search.stats.main import StatsSearch


class Factory:
    """
    ============================================================================
     Factory for StatsSearch.
    ============================================================================
    """

    @staticmethod
    def linear() -> StatsSearch:
        """
        ========================================================================
         Factory of a linear stats.
        ========================================================================
        """
        return StatsSearch(generated=10, explored=20)