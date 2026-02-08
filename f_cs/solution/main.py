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
                 problem: Problem,
                 is_valid: bool,
                 stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=is_valid)
        self._stats: Stats = stats
        self._problem: Problem = problem

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
    