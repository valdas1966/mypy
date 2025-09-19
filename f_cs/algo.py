from f_core.processes.i_2_io import ProcessIO
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo, StatsAlgo
from abc import abstractmethod
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo[StatsAlgo])


class Algo(Generic[Problem, Solution],
           ProcessIO[Problem, Solution]):
    """
    ============================================================================
     ABC for Algorithm.
    ============================================================================
    """
    def __init__(self,
                 problem: ProblemAlgo,
                 verbose: bool = False,
                 name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem.clone()
        ProcessIO.__init__(self,
                           _input=self._problem,
                           verbose=verbose, name=name)

    @abstractmethod
    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass
