from openpyxl.worksheet.worksheet import Worksheet


class HeightRow:
    """
    ============================================================================
     Manage the height of rows in an Excel worksheet.
    ----------------------------------------------------------------------------
     Usage:
    ----------------------------------------------------------------------------
        height_row = HeightRow(sheet)

        height = height_row[2]       # Get row height
        height_row[2] = 25           # Set row height
    ============================================================================
    """

    DEFAULT = 15.0

    def __init__(self, sheet: Worksheet) -> None:
        """
        ========================================================================
         Initialize the Height-Row component.
        ========================================================================
        """
        self._sheet = sheet

    def __getitem__(self, row: int) -> float:
        """
        ========================================================================
         1. Get the height of a row.
         2. If the height is not set, return the default height.
        ========================================================================
        """
        return self._sheet.row_dimensions[row].height or self.DEFAULT

    def __setitem__(self, row: int, height: float) -> None:
        """
        ========================================================================
         Set the height of a row.
        ========================================================================
        """
        self._sheet.row_dimensions[row].height = height
