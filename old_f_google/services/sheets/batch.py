from gspread import Worksheet
from gspread import Cell


class Batch:
    """
    ============================================================================
     Manage Batch of Cell-Updates.
    ============================================================================
    """

    def __init__(self, ws: Worksheet) -> None:
        self._ws = ws
        self._cells: list[Cell] = list()

    def add(self, cell: Cell) -> None:
        """
        ========================================================================
         Add Cell-Update to Batch.
        ========================================================================
        """
        self._cells.append(cell)

    def run(self) -> None:
        """
        ========================================================================
         Update the Cells-Data into the Google-Sheet.
        ========================================================================
        """
        # Update the Cells in the Google Sheets
        self._ws.update_cells(self._cells)
        # Reset the Cells-List of the Batch
        self._cells: list[Cell] = list()
