from f_search.heuristics.aggregative.main import HeuristicsAggregative
from f_search.ds.state import StateCell as State


class Factory:
    """
    ============================================================================
     Factory for creating HeuristicsAggregative objects.
    ============================================================================
    """

    @staticmethod
    def cell_01_10() -> HeuristicsAggregative:
        """
        ========================================================================
         Return HeuristicsAggregative object for cells 01 and 10.
        ========================================================================
        """
        state_01 = State.Factory.cell_01()
        state_10 = State.Factory.cell_10()
        goals_active = [state_01, state_10]
        return HeuristicsAggregative[State](goals_active=goals_active)
    