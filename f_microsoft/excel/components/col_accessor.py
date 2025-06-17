from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter


class ColAccessor:
    """
    ============================================================================
     1. Col-Accessor component of Microsoft Excel Worksheet.
     2. Purpose: Access Column's properties (like width).
    ============================================================================
    """

    # Default width of a column in a Microsoft Excel Worksheet
    DEF_WIDTH = 8.43

    def __init__(self,
                 # Worksheet
                 sheet: Worksheet,
                 # Column index
                 index: int) -> None:
        """
        ========================================================================
         Initialize the Col-Accessor component.
        ========================================================================
        """
        # Worksheet to work with
        self._sheet = sheet
        # Column index
        self._index = index
        # Get the column letter (need for openpyxl col access)
        self._letter = get_column_letter(index)

    @property
    def width(self) -> float:
        """
        ========================================================================
         Return the width of the column.
        ========================================================================
        """
        return (self._sheet.column_dimensions[self._letter].width
                or ColAccessor.DEF_WIDTH)

    @width.setter
    def width(self, value: float) -> None:
        """
        ========================================================================
         Set the width of the column.
        ========================================================================
        """
        self._sheet.column_dimensions[self._letter].width = value
