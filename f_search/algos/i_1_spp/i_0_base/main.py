from f_search.algos.i_0_base.main import AlgoSearch
from f_search.ds.data import DataSPP
from f_search.stats import StatsSPP
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSPP)
Solution = TypeVar('Solution', bound=SolutionSPP) 
Stats = TypeVar('Stats', bound=StatsSPP)
Data = TypeVar('Data', bound=DataSPP)


class AlgoSPP(Generic[Problem, Solution, Stats, Data],
              AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    cls_stats = StatsSPP
    cls_data = DataSPP

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 verbose: bool = False,
                 name: str = 'AlgoSPP') -> None:
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
        