from f_search.ds.state import StateBase
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HeuristicsBase(ABC, Generic[State]):
    """
    ============================================================================
     Base-Class for Heuristics.
    ============================================================================
    """
    
    @abstractmethod
    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Heuristic-Value for the given State.
        ========================================================================
        """
        pass