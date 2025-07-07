from f_ds.grids.cell.map.main import CellMap


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
