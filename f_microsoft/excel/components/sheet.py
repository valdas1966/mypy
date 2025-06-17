from typing import Iterable
from openpyxl.worksheet.worksheet import Worksheet
from f_microsoft.excel.components.cell_proxy import CellProxy
from f_microsoft.excel.components.row_proxy import RowProxy
from f_microsoft.excel.components.col_proxy import ColProxy


class Sheet:
    """
    ============================================================================
     1. Sheet component of Microsoft Excel Worksheet.
     2. Purpose: Access Sheet's properties (like rows).
    ============================================================================
    """

    RATIO_HEIGHT_WIDTH = 5.4

    def __init__(self,
                 # Worksheet
                 sheet: Worksheet) -> None:
        """
        ========================================================================
         Initialize the Sheet component.
        ========================================================================
        """
        # Worksheet to work with
        self._sheet = sheet
        # Row Proxy
        self._row = RowProxy(sheet=sheet)
        # Column Proxy
        self._col = ColProxy(sheet=sheet)

    @property
    def row(self) -> RowProxy:
        """
        ========================================================================
         Return the Row-Proxy component.
        ========================================================================
        """
        return self._row

    @property
    def col(self) -> ColProxy:
        """
        ========================================================================
         Return the Column-Proxy component.
        ========================================================================
        """
        return self._col
    
    @property
    def title(self) -> str:
        """
        ========================================================================
         Return the title of the sheet.
        ========================================================================
        """
        return self._sheet.title
    
    @title.setter
    def title(self,
              # New Title
              value: str) -> None:
        """
        ========================================================================
         Set the title of the sheet.
        ========================================================================
        """
        self._sheet.title = value   

    def set_rows_height(self,
                        # Rows to set the height
                        rows: Iterable[int],
                        # Height to set
                        height: float) -> None:
        """
        ========================================================================
         Set the height of the given rows.
        ========================================================================
        """
        for row in rows:
            self.row[row].height = height

    def set_cols_width(self,
                       # Columns to set the width
                       cols: Iterable[int],
                       # Width to set
                       width: float) -> None:
        """
        ========================================================================
         Set the width of the given columns.
        ========================================================================
        """
        for col in cols:
            self.col[col].width = width

    def __getitem__(self, row: int) -> CellProxy:
        """
        ========================================================================
         Return the CellProxy at the given row.
        ========================================================================
        """
        return CellProxy(sheet=self._sheet,
                         row=row)