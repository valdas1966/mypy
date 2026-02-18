from f_search.heuristics import HeuristicsProtocol
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HeuristicsAggregative(HeuristicsProtocol[State], Generic[State]):
    """
    ============================================================================
     Aggregative Heuristic [MIN].
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, goals_active: list[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals_active = goals_active

    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Aggregative Heuristic-Value for the given State.
        ========================================================================
        """
        return min(state.distance(other=goal) for goal in self._goals_active)
