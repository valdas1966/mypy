from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.state.i_1_cell.main import StateCell as State
from f_search.ds.frontier import FrontierFifo


class Factory:
    """
    ============================================================================
     Factory for creating DataBestFirst objects.
    ============================================================================
    """
    
    @staticmethod
    def empty() -> DataBestFirst:
        """
        ========================================================================
         Create a DataBestFirst object with an empty Frontier.
        ========================================================================
        """
        frontier = FrontierFifo()
        return DataBestFirst(frontier=frontier)

    @staticmethod
    def cell_00() -> DataBestFirst:
        """
        ========================================================================
         Create a DataBestFirst object with a cell_00 Frontier.
        ========================================================================
        """
        state_00 = State.Factory.zero()
        state_01 = State.Factory.cell_01()
        state_10 = State.Factory.cell_10()
        explored = {state_00}
        frontier = FrontierFifo.Factory.cells_01_10()
        dict_parent = {state_00: None,
                       state_01: state_00,
                       state_10: state_00}
        dict_g = {state_00: 0, state_01: 1, state_10: 1}
        return DataBestFirst(frontier=frontier,
                             explored=explored,
                             dict_parent=dict_parent,
                             dict_g=dict_g)
