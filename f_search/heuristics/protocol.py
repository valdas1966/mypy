from typing import Protocol, TypeVar
from f_search.ds.state import StateBase

State = TypeVar('State', bound=StateBase)


class HeuristicsProtocol(Protocol[State]):
    """
    ============================================================================
     Protocol for a function that returns the heuristic value of a given state.
    ============================================================================
    """

    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Heuristic-Value for the given State.
        ========================================================================
        """
        ...
