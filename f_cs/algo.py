from f_core.processes.i_2_io import ProcessIO
from f_cs.solution import SolutionAlgo
from f_cs.problem import ProblemAlgo
from f_cs.stats import StatsAlgo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo)


class Algo(Generic[Problem, Solution], ProcessIO[Problem, Solution]):
    """
    ============================================================================
     Bace class for Algorithm in Computer-Science.
    ============================================================================
    """

    cls_stats: type[StatsAlgo] = StatsAlgo

    def __init__(self,
                 problem: Problem,
                 name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(input=problem, name=name)
        self._stats: StatsAlgo = self.cls_stats()

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the Problem of the Algorithm.
        ========================================================================
        """
        return self.input

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the Algorithm finishes.
        ========================================================================
        """
        super()._run_post()
        self._stats.elapsed = self.elapsed
