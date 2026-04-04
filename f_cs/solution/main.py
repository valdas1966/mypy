from f_core.mixins.validatable.main import Validatable
from f_core.recorder import Recorder
from f_cs.problem.main import ProblemAlgo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemAlgo)


class SolutionAlgo(Generic[Problem], Validatable):
    """
    ============================================================================
     ABC for Algorithm's Solution.
    ============================================================================
    """

    def __init__(self,
                 name_algo: str,
                 problem: Problem,
                 is_valid: bool,
                 elapsed: float = 0,
                 recorder: Recorder | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=is_valid)
        self._name_algo: str = name_algo
        self._problem: Problem = problem
        self._elapsed: float = elapsed
        self._recorder: Recorder = (recorder if recorder
                                    else Recorder())

    @property
    def name_algo(self) -> str:
        """
        ========================================================================
         Return the Algorithm's Name.
        ========================================================================
        """
        return self._name_algo

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the Problem of the Solution.
        ========================================================================
        """
        return self._problem

    @property
    def elapsed(self) -> float:
        """
        ========================================================================
         Return the elapsed time in seconds.
        ========================================================================
        """
        return self._elapsed

    @property
    def recorder(self) -> Recorder:
        """
        ========================================================================
         Return the Recorder with recorded Events.
        ========================================================================
        """
        return self._recorder
