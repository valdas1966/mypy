from f_graph.problems.i_0_graph import ProblemGraph
from abc import ABC, abstractmethod
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemGraph)


class TerminationBase(ABC):
    """
    ============================================================================
     Abstract Class for Termination process of Graph-Algorithm.
    ============================================================================
    """

    @abstractmethod
    def can(self, *args) -> bool:
        """
        ========================================================================
         Return True if the Search-Process can be Terminated.
        ========================================================================
        """
        pass
