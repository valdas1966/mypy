from f_search.heuristics.manhattan.main import HeuristicsManhattan
from f_search.ds.state.i_1_cell.main import StateCell as State


class Factory:
    """
    ============================================================================
     Factory for creating HeuristicsManhattan objects.
    ============================================================================
    """

    @staticmethod
    def cell_01() -> HeuristicsManhattan:
        """
        ========================================================================
         Return HeuristicsManhattan object for cells 01 and 10.
        ========================================================================
        """
        state_01 = State.Factory.cell_01()
        return HeuristicsManhattan[State](goal=state_01)
