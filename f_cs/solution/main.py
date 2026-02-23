from f_core.mixins.validatable.main import Validatable
from f_cs.problem.main import ProblemAlgo
from f_cs.stats.main import StatsAlgo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)
Stats = TypeVar('Stats', bound=StatsAlgo)


class SolutionAlgo(Generic[Problem, Stats], Validatable):
    """
    ============================================================================
     ABC for Algorithm's Solution.
    ============================================================================
    """

    def __init__(self,
                 name_algo: str,
                 problem: Problem,
                 is_valid: bool,
                 stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=is_valid)
        self._name_algo: str = name_algo
        self._stats: Stats = stats
        self._problem: Problem = problem

    @property
    def name_algo(self) -> str:
        """
        ========================================================================
         Return the Algorithm's Name.
        ========================================================================
        """
        return self._name_algo

    @property
    def stats(self) -> Stats:
        """
        ========================================================================
         Return the Algorithm's Stats.
        ========================================================================
        """
        return self._stats

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the Problem of the Solution.
        ========================================================================
        """
        return self._problem
    