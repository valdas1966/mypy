from f_core.processes.i_2_io import ProcessIO
from old_f_cs.solution.main import SolutionAlgo
from old_f_cs.problem.main import ProblemAlgo
from old_f_cs.stats.main import StatsAlgo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo)


class Algo(Generic[Problem, Solution], ProcessIO[Problem, Solution]):
    """
    ============================================================================
     Base class for Algorithm in Computer-Science.
    ============================================================================
    """

    cls_stats: type[StatsAlgo] = StatsAlgo

    def __init__(self,
                 problem: Problem,
                 name: str = 'Algorithm',
                 is_recording: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(input=problem, name=name,
                         is_recording=is_recording)
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
