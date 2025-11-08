from f_cs.solution import SolutionAlgo
from f_search.stats import StatsSearch
from typing import Generic, TypeVar

Stats = TypeVar('Stats', bound=StatsSearch)


class SolutionSearch(Generic[Stats], SolutionAlgo[Stats]):
    """
    ============================================================================
     Solution for Search-Problems.
    ============================================================================
    """
    def __init__(self,
                 is_valid: bool,
                 stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=is_valid, stats=stats)
