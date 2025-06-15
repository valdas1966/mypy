from openpyxl.worksheet.worksheet import Worksheet
from f_microsoft.excel.components.width_col import WidthCol
from f_microsoft.excel.components.height_row import HeightRow


class Layout:
    """
    ============================================================================
     1. Layout component for managing heights and widths in a worksheet.
     2. Usage:
    ----------------------------------------------------------------------------
     layout = Layout(sheet)

     layout.width_col[1] = 20      # Set column width
     layout.height_row[2] = 25     # Set row height
     width = layout.width_col[1]   # Get column width
     height = layout.height_row[2] # Get row height
    ============================================================================
    """

    def __init__(self, sheet: Worksheet) -> None:
        """
        ========================================================================
         Initialize the Layout component.
        ========================================================================
        """
        self._sheet = sheet
        self._width_col = WidthCol(sheet=sheet)
        self._height_row = HeightRow(sheet=sheet)
        
    @property
    def width_col(self) -> WidthCol:
        """
        ========================================================================
         Get the width of a column.
        ========================================================================
        """
        return self._width_col
    
    @property
    def height_row(self) -> HeightRow:
        """
        ========================================================================
         Get the height of a row.
        ========================================================================
        """
        return self._height_row

    