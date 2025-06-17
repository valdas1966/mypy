from f_microsoft.excel.components.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


class CellProxy:
    """
    ============================================================================
     1. CellProxy component of Microsoft Excel Worksheet.
     2. Purpose: Access Cell's properties (like value).
     3. Receives a Row-Index in Init() and needs a Col-Index to return a Cell.
    ============================================================================
    """

    def __init__(self,
                 # Worksheet to work with
                 sheet: Worksheet,
                 # Row Index
                 row: int) -> None:
        """
        ========================================================================
         Initialize the CellProxy component.
        ========================================================================
        """
        self._sheet = sheet
        self._row = row

    def __getitem__(self, col: int) -> Cell:
        """
        ========================================================================
         Return the Cell at the given column.
        ========================================================================
        """
        return Cell(sheet=self._sheet,
                    row=self._row,
                    col=col)
