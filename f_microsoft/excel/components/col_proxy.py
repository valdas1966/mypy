from openpyxl.worksheet.worksheet import Worksheet
from f_microsoft.excel.components.col_accessor import ColAccessor


class ColProxy:
    """
    ============================================================================
     1. Col-Proxy component of Microsoft Excel Worksheet.
     2. Purpose: Proxy for accessing Column's properties (like width).
    ============================================================================
    """

    def __init__(self,
                 # Worksheet to work with
                 sheet: Worksheet) -> None:
        """
        ========================================================================
         Initialize the Col-Proxy component.
        ========================================================================
        """
        self._sheet = sheet

    def __getitem__(self,
                    # Column index
                    index: int) -> ColAccessor:
        """
        ========================================================================
         Return the Col-Accessor component.
        ========================================================================
        """
        return ColAccessor(sheet=self._sheet, index=index)
