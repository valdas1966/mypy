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

    Factory = None
    
    def __init__(self,
                 is_valid: bool,
                 stats: Stats,
                 name: str = 'SolutionSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=is_valid, stats=stats, name=name)
