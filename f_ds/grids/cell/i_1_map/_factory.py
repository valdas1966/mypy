from f_ds.grids.cell.i_1_map.main import CellMap


class Factory:
    """
    ============================================================================
     Factory-Class for the CellMap.
    ============================================================================
    """
    
    @staticmethod
    def zero() -> CellMap:
        """
        ========================================================================
         Return a new CellMap with the row and col set to 0.
        ========================================================================
        """
        return CellMap(row=0, col=0)

    @staticmethod
    def one() -> CellMap:
        """
        ========================================================================
         Return a new CellMap with the row and col set to 1.
        ========================================================================
        """
        return CellMap(row=1, col=1)
    
    @staticmethod
    def million() -> CellMap:
        """
        ========================================================================
         Return a new CellMap with the row and col set to 1000000.
        ========================================================================
        """
        return CellMap(row=1_000_000, col=1_000_000)
