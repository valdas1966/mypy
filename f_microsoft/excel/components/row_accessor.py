from openpyxl.worksheet.worksheet import Worksheet


class RowAccessor:
    """
    ============================================================================
     1. Row-Accessor component of Microsoft Excel Worksheet.
     2. Purpose: Access Row's properties (like height).
    ============================================================================
    """

    DEF_HEIGHT = 15.0

    def __init__(self,
                 # Worksheet
                 sheet: Worksheet,
                 # Row index
                 index: int) -> None:
        """
        ========================================================================
         Initialize the Row-Accessor component.
        ========================================================================
        """
        self._sheet = sheet
        self._index = index

    @property
    def height(self) -> float:
        """
        ========================================================================
         Return the height of the row.
        ========================================================================
        """
        return (self._sheet.row_dimensions[self._index].height
                or RowAccessor.DEF_HEIGHT)

    @height.setter
    def height(self,
               # New Height
               value: float) -> None:
        """
        ========================================================================
         Set the height of the row.
        ========================================================================
        """
        self._sheet.row_dimensions[self._index].height = value
