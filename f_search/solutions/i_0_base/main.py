from f_cs.solution.main import SolutionAlgo
from f_search.problems import ProblemSearch
from f_search.stats import StatsSearch
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSearch)
Stats = TypeVar('Stats', bound=StatsSearch)


class SolutionSearch(Generic[Problem, Stats], SolutionAlgo[Problem, Stats]):
    """
    ============================================================================
     Solution for Search-Problems.
    ============================================================================
    """

    Factory = None
    
    def __init__(self,
                 name_algo: str,
                 problem: Problem,
                 is_valid: bool,
                 stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self,
                              name_algo=name_algo,
                              problem=problem.to_light(),
                              is_valid=is_valid,
                              stats=stats)
