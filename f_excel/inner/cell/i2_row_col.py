import openpyxl.worksheet
from f_excel.inner.cell.i1_init import MyCellInit


class MyCellRowCol(MyCellInit):
    """
    ============================================================================
     Desc: Return Row and Col indexes of the Cell.
    ============================================================================
    """

    @property
    def row(self):
        """
        ========================================================================
         Description: Return the Row-Index of the Cell.
        ========================================================================
        """
        return self._cell.row

    @property
    def col(self):
        """
        ========================================================================
         Description: Return the Col-Index of the Cell.
        ========================================================================
        """
        return self._cell.column
