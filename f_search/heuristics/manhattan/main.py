from f_search.heuristics.protocol import HeuristicsProtocol
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)

class HeuristicsManhattan(HeuristicsProtocol[State], Generic[State]):
    """
    ============================================================================
     Heuristics represented Manhattan-Distance between State and Goal.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, goal: State) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal

    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Manhattan-Distance between State and Goal.
        ========================================================================
        """
        return state.distance(other=self._goal)
