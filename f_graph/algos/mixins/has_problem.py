from f_graph.problems.i_1_path import ProblemPath
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)


class HasProblem:
    """
    ============================================================================
     Mixin-Classes for Algorithms with Path-Problems.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return Algorithm's Path-Problem.
        ========================================================================
        """
        return self._problem
