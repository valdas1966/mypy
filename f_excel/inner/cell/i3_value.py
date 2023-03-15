from f_excel.inner.cell.i2_row_col import MyCellRowCol


class MyCellValue(MyCellRowCol):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Gets and Sets the Cells' Value.
        2. Empties the Cell (from Value).
        3. Checks if the Cell is Empty.
    ============================================================================
    """

    @property
    def value(self) -> any:
        """
        ========================================================================
         Description: Return the Value of the Cell.
        ========================================================================
        """
        return self._cell.value

    @value.setter
    def value(self, val: any) -> None:
        """
        ========================================================================
         Description: Set the Value of the Cell.
        ========================================================================
        """
        self._cell.value = val

    def empty(self) -> None:
        """
        ========================================================================
         Description: Empty the Cell's Value.
        ========================================================================
        """
        self._cell.value = None

    def is_empty(self) -> bool:
        """
        ========================================================================
         Description: Return True if the Cell's Value is Empty.
        ========================================================================
        """
        return self._cell.value in (None, '')
