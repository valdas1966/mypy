from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.stats import StatsOOSPP
from f_search.ds.path import Path


class SolutionOOSPP(SolutionSearch[StatsOOSPP]):
    """
    ============================================================================
     Solution for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    def __init__(self,
                 is_valid: bool,
                 stats: StatsOOSPP,
                 path: Path) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
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
