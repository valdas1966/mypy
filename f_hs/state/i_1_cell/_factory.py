from f_hs.state import StateCell as State
from f_ds.grids import CellMap as Cell


class Factory:
    """
    ========================================================================
     Factory for StateCell test instances.
    ========================================================================
    """

    @staticmethod
    def at(row: int, col: int = None) -> State:
        """
        ====================================================================
         Create a StateCell at the given (row, col).
        ====================================================================
        """
        col = row if col is None else col
        cell = Cell(row=row, col=col)
        return State(key=cell)
