from old_f_logging.dec import log_all_methods, log_info_class
from f_excel.model.ws.base import MyExcelWorkSheet
from f_excel.model.cell.prod import MyExcelCell
import openpyxl.worksheet


@log_all_methods(decorator=log_info_class)
class MyExcelWorkSheetCells(MyExcelWorkSheet):
    """
    ============================================================================
     Description:
    ----------------------------------------------------------------------------
        1. Represents the Excel-Worksheet.
        2. Initializes with the openpyxl.worksheet object.
        3. Can return MyExcelCell object by its indexes (eg: ws[1,2]).
    ============================================================================
    """

    def __init__(self, ws: openpyxl.worksheet):
        """
        ========================================================================
         Description: Constructor. Call the Super().
        ========================================================================
        """
        super().__init__(ws=ws)

    def __getitem__(self, item: tuple[int, int]) -> any:
        """
        ========================================================================
         Description: Return the Str-Representation of the Cell-Value in the
                       given coordinates (row, col).
        ========================================================================
        """
        row, col = item
        cell = self._ws.cell(row, col)
        return MyExcelCell(cell=cell)
