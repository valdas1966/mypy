from f_cs.solution import SolutionAlgo
from f_search.stats import StatsOOSPP
from f_search.path import Path


class SolutionOOSPP(SolutionAlgo[StatsOOSPP]):
    """
    ============================================================================
     Solution for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 path: Path,
                 stats: StatsOOSPP) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self,
                              is_valid=is_valid,
                              stats=stats)
        self._path = path
    
    @property
    def path(self) -> Path:
        """
        ========================================================================
         Return the Solution's Path.
        ========================================================================
        """
        return self._path