from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from f_abstract.mixins.validatable import Validatable
from f_graph.problems.i_1_path import ProblemPath, NodePath

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodePath)


class PathBase(ABC, Generic[Problem, Node], Validatable):
    """
    ============================================================================
     Base-Class of Path for Path-Algorithms.
    ============================================================================
    """

    def __init__(self, problem: Problem):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=False)
        self._problem = problem

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return Path-Problem.
        ========================================================================
        """
        return self._problem

    @abstractmethod
    def get(self) -> list[Node]:
        """
        ========================================================================
         Return a Path.
        ========================================================================
        """
        pass
