from f_cs.algo import Algo
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from f_search.ds.data import DataSearch
from typing import Generic, TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)
Stats = TypeVar('Stats', bound=StatsSearch)
Data = TypeVar('Data', bound=DataSearch)


class AlgoSearch(Generic[Problem, Solution, Stats, Data],
                 Algo[Problem, Solution, Stats]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """

    cls_stats: Type[Stats] = StatsSearch
    cls_data: Type[Data] = DataSearch

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 verbose: bool = False,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, verbose=verbose, name=name)
        self._data = data if data else self.cls_data()
