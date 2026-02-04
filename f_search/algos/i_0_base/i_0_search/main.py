from f_cs.algo.main import Algo
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)


class AlgoSearch(Generic[Problem, Solution], Algo[Problem, Solution]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """

    cls_stats: type[StatsSearch] = StatsSearch

    def __init__(self,
                 problem: Problem,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
