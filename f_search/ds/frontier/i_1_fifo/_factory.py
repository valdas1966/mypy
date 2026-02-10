from f_search.ds.frontier.i_1_fifo.main import FrontierFifo
from f_search.ds.state.i_1_cell.main import StateCell as State
from f_ds.grids.cell.i_1_map import CellMap as Cell


class Factory:
    """
    ============================================================================
     Factory for creating Frontier objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> FrontierFifo:
        """
        ========================================================================
         Create a FrontierFifo object with the 'A', 'B', 'C' state.
        ========================================================================
        """
        frontier = FrontierFifo[str]()
        frontier.push(state='A')
        frontier.push(state='B')
        frontier.push(state='C')
        return frontier

    @staticmethod
    def cells_01_10() -> FrontierFifo[State]:
        """
        ========================================================================
         Create a FrontierFifo object with the cells (0, 1) and (1, 0).
        ========================================================================
        """
        state_01 = State.Factory.cell_01()
        state_10 = State.Factory.cell_10()
        frontier = FrontierFifo[State]()
        frontier.push(state=state_01)
        frontier.push(state=state_10)
        return frontier
