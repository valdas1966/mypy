from f_hs.state.i_1_cell.main import StateCell
from f_ds.grids.cell.i_1_map import CellMap


class Factory:
    """
    ========================================================================
     Factory for StateCell test instances.
    ========================================================================
    """

    @staticmethod
    def at(row: int, col: int) -> StateCell:
        """
        ====================================================================
         Create a StateCell at the given (row, col).
        ====================================================================
        """
        return StateCell(key=CellMap(row=row, col=col))

    @staticmethod
    def origin() -> StateCell:
        """
        ====================================================================
         Create a StateCell at (0, 0).
        ====================================================================
        """
        return StateCell(key=CellMap(row=0, col=0))

    @staticmethod
    def a() -> StateCell:
        """
        ====================================================================
         Create a StateCell at (0, 0).
        ====================================================================
        """
        return StateCell(key=CellMap(row=0, col=0))

    @staticmethod
    def b() -> StateCell:
        """
        ====================================================================
         Create a StateCell at (2, 2).
        ====================================================================
        """
        return StateCell(key=CellMap(row=2, col=2))
