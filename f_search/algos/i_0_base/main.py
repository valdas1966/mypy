from f_cs.algo import Algo
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from f_search.ds.data.search import DataSearch
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)


class AlgoSearch(Generic[Problem, Solution],
                 Algo[Problem, Solution]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, verbose=verbose, name=name)

    def _run_pre(self) -> None:
        """
        ========================================================================
         Init data structures.
        ========================================================================
        """
        Algo._run_pre(self)
        self._data = DataSearch()
        self._stats: StatsSearch = None
