from gspread.worksheet import Worksheet
from gspread.cell import Cell as GSCell
from f_google.sheets.batch import Batch
from f_google.sheets.cell import Cell


class Sheet:
    """
    ============================================================================
     Google-Sheets WorkSheet.
    ============================================================================
    """

    def __init__(self, ws: Worksheet) -> None:
        self._ws = ws
        self._batch = Batch(ws=ws)

    @property
    def title(self) -> str:
        return self._ws.title

    @property
    def index(self) -> int:
        return self._ws.index

    def update(self) -> None:
        """
        ========================================================================
         Update the Google-Sheet with the updates in the Batch.
        ========================================================================
        """
        self._batch.run()

    def __getitem__(self, coords: tuple[int, int]) -> Cell:
        row, col = coords
        gs_cell: GSCell = self._ws.cell(row, col)
        return Cell(cell=gs_cell, add_to_batch=self._batch.add)
