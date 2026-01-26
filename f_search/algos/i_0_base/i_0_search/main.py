from f_cs.algo import Algo
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from typing import Generic, TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)
Stats = TypeVar('Stats', bound=StatsSearch)


class AlgoSearch(Generic[Problem, Solution, Stats],
                 Algo[Problem, Solution, Stats]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """

    cls_stats: Type[Stats] = StatsSearch

    def __init__(self,
                 problem: Problem,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._stats = self.cls_stats()
        