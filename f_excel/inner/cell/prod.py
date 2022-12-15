from f_logging.dec import log_all_methods, log_info_class
from f_excel.model.cell.value import MyExcelCellValue
import openpyxl.worksheet


@log_all_methods(decorator=log_info_class)
class MyExcelCell(MyExcelCellValue):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Represents the Excel-Cell.
        2. Initializes with the Cell-Object of the openpyxl Package.
    ============================================================================
    """

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        """
        ========================================================================
         Description: Constructor. Initializes the Super().
        ========================================================================
        """
        super().__init__(cell=cell)
