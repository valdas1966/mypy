from f_search.algos.i_0_base.main import AlgoSearch
from f_search.solutions import SolutionOMSPP
from f_search.problems import ProblemOMSPP
from f_search.stats import StatsOMSPP
from f_search.ds.data import DataOMSPP
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemOMSPP)
Solution = TypeVar('Solution', bound=SolutionOMSPP)
Stats = TypeVar('Stats', bound=StatsOMSPP)
Data = TypeVar('Data', bound=DataOMSPP)


class AlgoOMSPP(Generic[Problem, Solution, Stats, Data],
                AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for One-to-Many Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    cls_stats = StatsOMSPP
    cls_data = DataOMSPP

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 verbose: bool = True,
                 name: str = 'AlgoOMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            data=data,
                            verbose=verbose,
                            name=name)
