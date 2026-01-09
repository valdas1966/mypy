from f_search.algos.i_0_base import AlgoSearch
from f_search.ds.data import DataSearch
from f_search.stats import StatsSearch
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSPP)
Solution = TypeVar('Solution', bound=SolutionSPP) 
Stats = TypeVar('Stats', bound=StatsSearch)
Data = TypeVar('Data', bound=DataSearch)


class AlgoSPP(Generic[Problem, Solution, Stats, Data],
              AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    cls_stats = StatsSearch
    cls_data = DataSearch

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 name: str = 'AlgoSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data,
                         name=name)
        