from f_search.ds.state.i_1_cell.main import StateCell
from f_ds.grids.cell import CellMap as Cell


class Factory:
    """
    ============================================================================
     Factory for creating States.
    ============================================================================
    """

    @staticmethod
    def zero() -> StateCell:
        """
        ========================================================================
         Return a new StateCell with the cell (0, 0).
        ========================================================================
        """
        cell = Cell(0, 0)
        return StateCell(key=cell, name='Zero')

    @staticmethod
    def one() -> StateCell:
        """
        ========================================================================
         Return a new StateCell with the cell (1, 1).
        ========================================================================
        """
        cell = Cell(1, 1)
        return StateCell(key=cell, name='One')

    @staticmethod
    def two() -> StateCell:
        """
        ========================================================================
         Return a new StateCell with the cell (2, 2).
        ========================================================================
        """
        cell = Cell(2, 2)
        return StateCell(key=cell, name='Two')
    
    @staticmethod
    def million() -> StateCell:
        """
        ========================================================================
         Return a new StateCell with the cell (1000000, 1000000).
        ========================================================================
        """
        cell = Cell.Factory.million()
        return StateCell(key=cell, name='Million')
