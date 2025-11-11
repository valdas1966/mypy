from f_ds.grids.cell.i_1_map import CellMap as Cell
from f_search.ds.state.main import State


class Factory:
    """
    ============================================================================
     Factory for creating States.
    ============================================================================
    """

    @staticmethod
    def zero() -> State[Cell]:
        """
        ========================================================================
         Return a new State with the cell (0, 0).
        ========================================================================
        """
        cell = Cell(0, 0)
        return State(key=cell)

    @staticmethod
    def one() -> State[Cell]:
        """
        ========================================================================
         Return a new State with the cell (1, 1).
        ========================================================================
        """
        cell = Cell(1, 1)
        return State(key=cell)

    @staticmethod
    def two() -> State[Cell]:
        """
        ========================================================================
         Return a new State with the cell (2, 2).
        ========================================================================
        """
        cell = Cell(2, 2)
        return State(key=cell)
