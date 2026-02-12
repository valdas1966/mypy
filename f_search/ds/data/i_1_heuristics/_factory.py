from f_search.ds.data.i_1_heuristics.main import DataHeuristics
from f_search.ds.state.i_1_cell.main import StateCell as State
from f_search.ds.frontier.i_1_priority import FrontierPriority


class Factory:
    """
    ============================================================================
     Factory for creating DataHeuristics objects.
    ============================================================================
    """

    @staticmethod
    def cell_00() -> DataHeuristics:
        """
        ========================================================================
         Create a DataHeuristics object with a cell_00 Frontier.
        ========================================================================
        """
        state_00 = State.Factory.zero()
        state_01 = State.Factory.cell_01()
        state_10 = State.Factory.cell_10()
        explored = {state_00}
        frontier = FrontierPriority.Factory.cells_01_10()
        dict_parent = {state_00: None,
                       state_01: state_00,
                       state_10: state_00}
        dict_g = {state_00: 0, state_01: 1, state_10: 1}
        dict_h = {state_00: 3, state_01: 2, state_10: 4}
        return DataHeuristics(explored=explored,
                              frontier=frontier,
                              dict_parent=dict_parent,
                              dict_g=dict_g,
                              dict_h=dict_h)
