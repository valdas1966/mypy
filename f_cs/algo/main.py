from f_core.processes.i_2_io import ProcessIO
from f_cs.solution.main import SolutionAlgo
from f_cs.problem.main import ProblemAlgo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)
Solution = TypeVar('Solution', bound=SolutionAlgo)


class Algo(Generic[Problem, Solution], ProcessIO[Problem, Solution]):
    """
    ============================================================================
     Base class for Algorithm in Computer-Science.
    ============================================================================
    """

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

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the Problem of the Algorithm.
        ========================================================================
        """
        return self.input
