from f_logging.dec import log_all_methods, log_info_class
from f_excel.model.cell.base import MyExcelCell
import openpyxl.worksheet


@log_all_methods(decorator=log_info_class)
class MyExcelCellValue(MyExcelCell):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Represents the Excel-Cell.
        2. Initializes with the Cell-Object of the openpyxl Package.
        3. Gets and Sets the Cells' Value.
        4. Empties the Cell (from Value) and Checks if the Cell is Empty.
    ============================================================================
    """

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        """
        ========================================================================
         Description: Constructor. Initializes the Super().
        ========================================================================
        """
        super().__init__(cell=cell)

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
        val = self._cell.value
        return val is None or val == ''
