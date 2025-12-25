from f_core.processes.i_2_io import ProcessIO
from f_cs.solution import SolutionAlgo
from f_cs.problem import ProblemAlgo
from f_cs.stats import StatsAlgo
from typing import Generic, TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo[StatsAlgo])
Stats = TypeVar('Stats', bound=StatsAlgo)


class Algo(Generic[Problem, Solution, Stats],
           ProcessIO[Problem, Solution]):
    """
    ============================================================================
     ABC for Algorithm.
    ============================================================================
    """

    cls_stats: Type[Stats] = StatsAlgo

    def __init__(self,
                 problem: Problem,
                 verbose: bool = False,
                 name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        ProcessIO.__init__(self,
                           input=self._problem,
                           verbose=verbose,
                           name=name)
        self._stats = self.cls_stats()

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the Algorithm finishes.
        ========================================================================
        """
        ProcessIO._run_post(self)
        self._stats.elapsed = self._elapsed
