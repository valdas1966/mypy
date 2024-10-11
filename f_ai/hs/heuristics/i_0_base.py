from f_graph.problems.i_1_path import ProblemPath
from f_ai.hs.nodes.i_1_f import NodeF
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodeF)


class HeuristicsBase(ABC, Generic[Problem, Node]):
    """
    ============================================================================
     Base-Class for Heuristics.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem

    @abstractmethod
    def eval(self, node: Node) -> int:
        """
        ========================================================================
         Evaluate Heuristic to a given Node.
        ========================================================================
        """
        pass
