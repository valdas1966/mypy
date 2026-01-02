from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.stats import StatsSearch
from f_search.ds.path import Path


class SolutionSPP(SolutionSearch[StatsSearch]):
    """
    ============================================================================
     Solution for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 is_valid: bool,
                 path: Path,
                 stats: StatsSearch = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        stats = stats if stats else StatsSearch()
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._path = path
    
    @property
    def path(self) -> Path:
        """
        ========================================================================
         Return the Solution's Path.
        ========================================================================
        """
        return self._path
