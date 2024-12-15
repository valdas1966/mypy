from gspread.worksheet import Worksheet
from gspread.cell import Cell as GSCell
from f_google.services.sheets.batch import Batch
from f_google.services.sheets.cell import Cell
from f_google.services.sheets.u_sheet import USheet


class Sheet:
    """
    ============================================================================
     Google-Sheets WorkSheet.
    ============================================================================
    """

    __ROW_MAX = 1000

    def __init__(self, ws: Worksheet) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._ws = ws
        self._batch = Batch(ws=ws)

    @property
    def title(self) -> str:
        return self._ws.title

    @property
    def index(self) -> int:
        return self._ws.index

    def get_row_last(self, col: int, row_first: int = 1) -> int:
        """
        ========================================================================
         Return the Last non-empty Row in the given Col.
        ========================================================================
        """
        if self[row_first, col].is_empty():
            return -1
        a1_range = USheet.to_a1_range(row_first=row_first,
                                      row_last=row_first+Sheet.__ROW_MAX,
                                      col_first=col,
                                      col_last=col)
        cells: list[GSCell] = self._ws.range(name=a1_range)
        for i in range(1, len(cells)-1):
            if cells[i].value == str() or cells[i].value is None:
                return cells[i].row - 1
        return -1

    def to_tuples(self,
                  col_first: int,
                  col_last: int,
                  row_first: int,
                  row_last: int = None) -> tuple:
        """
        ========================================================================
         Convert the Range-Values in given coordinates into Tuple of Tuples.
        ========================================================================
        """
        if not row_last:
            row_last = self.get_row_last(col=col_first, row_first=row_first)
        a1_range = USheet.to_a1_range(row_first=row_first,
                                      row_last=row_last,
                                      col_first=col_first,
                                      col_last=col_last)
        cells: list[GSCell] = self._ws.range(name=a1_range)
        num_cols = col_last - col_first + 1
        return tuple(
                        tuple(cell.value for cell in cells[i:i + num_cols])
                        for i in range(0, len(cells), num_cols)
                    )

    def update(self) -> None:
        """
        ========================================================================
         Update the Google-Sheet with the updates in the Batch.
        ========================================================================
        """
        self._batch.run()

    def __getitem__(self, rowcol: tuple[int, int]) -> Cell:
        """
        ========================================================================
         Return list Cell by given Coordinates.
        ========================================================================
        """
        row, col = rowcol
        gs_cell: GSCell = self._ws.cell(row, col)
        return Cell(cell=gs_cell, add_to_batch=self._batch.add)

