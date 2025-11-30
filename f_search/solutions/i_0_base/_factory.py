from f_search.solutions.i_0_base.main import SolutionSearch, StatsSearch


class Factory:
    """
    ============================================================================
     Factory for SolutionSearch.
    ============================================================================
    """

    @staticmethod
    def zero_valid() -> SolutionSearch:
        """
        ========================================================================
         Factory of a valid solution with zero stats.
        ========================================================================
        """
        stats = StatsSearch.Factory.linear()
        return SolutionSearch(is_valid=True, stats=stats)

    @staticmethod
    def zero_invalid() -> SolutionSearch:
        """
        ========================================================================
         Factory of an invalid solution with zero stats.
        ========================================================================
        """
        stats = StatsSearch.Factory.linear()
        return SolutionSearch(is_valid=False, stats=stats)

