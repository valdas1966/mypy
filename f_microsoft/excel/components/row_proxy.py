from f_microsoft.excel.components.row_accessor import RowAccessor
from openpyxl.worksheet.worksheet import Worksheet


class RowProxy:
    """
    ============================================================================
     1. Row-Proxy component of Microsoft Excel Worksheet.
     2. Purpose: Proxy for accessing Row's properties (like height).
    ============================================================================
    """

    def __init__(self, sheet: Worksheet) -> None:
        """
        ========================================================================
         Initialize the Row-Proxy component.
        ========================================================================
        """
        self._sheet = sheet

    def __getitem__(self, index: int) -> RowAccessor:
        """
        ========================================================================
         Return the Row-Accessor component.
        ========================================================================
        """
        return RowAccessor(sheet=self._sheet, index=index)