from f_search.algos.i_0_base.main import AlgoSearch
from f_search.stats import StatsOMSPP
from f_search.problems import ProblemOMSPP
from f_search.solutions import SolutionOMSPP
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemOMSPP)
Solution = TypeVar('Solution', bound=SolutionOMSPP)


class AlgoOMSPP(Generic[Problem, Solution],
                AlgoSearch[Problem, Solution]):
    """
    ============================================================================
     Base for One-to-Many Shortest-Path-Problem Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoOMSPP') -> None:
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
        AlgoSearch._run_pre(self)
        self._stats: StatsOMSPP = None
