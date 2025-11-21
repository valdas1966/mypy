from f_ds.grids.cell.i_0_base.main import CellBase


class Factory:
    """
    ============================================================================
     Factory for CellBase.
    ============================================================================
    """

    @staticmethod
    def zero() -> CellBase:
        """
        ========================================================================
         Return a new CellBase with the row and col set to 0.
        ========================================================================
        """
        return CellBase(row=0, col=0)
