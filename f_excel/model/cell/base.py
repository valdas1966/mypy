from f_logging.dec import log_all_methods, log_info_class
import openpyxl.worksheet


@log_all_methods(decorator=log_info_class)
class MyExcelCell:
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Represents the Excel-Cell.
        2. Initializes with the Cell-Object of the openpyxl Package.
        3. Return the Row and Col indexes of the Cell.
    ============================================================================
    """

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        """
        ========================================================================
         Description: Constructor. Init the Attributes.
        ========================================================================
        """
        self._cell = cell

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
