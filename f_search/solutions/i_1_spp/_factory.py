from f_search.solutions.i_1_spp.main import SolutionSPP, StatsSearch, Path


class Factory:
    """
    ============================================================================
     Factory for SolutionSPP.
    ============================================================================
    """

    @staticmethod
    def valid() -> SolutionSPP:
        """
        ========================================================================
         Factory of a valid solution.
        ========================================================================
        """
        stats = StatsSearch.Factory.linear()
        path = Path.Factory.ab()
        return SolutionSPP(is_valid=True, path=path, stats=stats)

    @staticmethod
    def invalid() -> SolutionSPP:
        """
        ========================================================================
         Factory of a valid solution.
        ========================================================================
        """
        stats = StatsSearch.Factory.linear()
        path = Path()
        return SolutionSPP(is_valid=False, path=path, stats=stats)
