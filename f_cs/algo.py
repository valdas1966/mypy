from f_core.processes.i_2_io import ProcessIO
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo, StatsAlgo
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
                    name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=problem, name=name)
