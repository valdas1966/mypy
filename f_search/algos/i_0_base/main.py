from f_cs.algo import Algo
from f_search.ds.cost import Cost
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch, State
from f_search.solutions import SolutionSearch
from typing import Generic, TypeVar, Iterable
from f_search.ds.data.search import DataSearch
from f_search.ds.data.state import DataState
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
        self._d_search: DataSearch = DataSearch()
        self._d_state: DataState = DataState()
        # Stats of the Algorithm
        self._stats: StatsSearch = None
