from f_search.ds.state import StateBase
from f_search.problems.i_0_base import ProblemSearch
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)

class HeuristicsBase(ABC, Generic[State, Problem]):
    """
    ============================================================================
     Base-Class for Heuristics.
    ============================================================================
    """
    
    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._problem = problem
    
    @abstractmethod
    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Heuristic-Value for the given State.
        ========================================================================
        """
        pass
