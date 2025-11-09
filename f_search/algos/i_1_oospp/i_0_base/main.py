from f_search.algos.i_0_base.main import AlgoSearch
from f_search.stats import StatsOOSPP
from f_search.problems import ProblemOOSPP
from f_search.solutions import SolutionOOSPP
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemOOSPP)
Solution = TypeVar('Solution', bound=SolutionOOSPP) 


class AlgoOOSPP(Generic[Problem, Solution],
                AlgoSearch[Problem, Solution]):
    """
    ============================================================================
     Base for One-to-One Shortest-Path-Problem Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoOOSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            verbose=verbose,
                            name=name)

    def _run_pre(self) -> None:
        """
        ========================================================================
         Init data structures.
        ========================================================================
        """
        AlgoSearch._pre_run(self)
        self._stats: StatsOOSPP = None
