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

    def last_row(self, col: int) -> int:
        """
        ========================================================================
         Return the Last non-empty Row in the given Col.
        ========================================================================
        """
        return len(self._ws.col_values(col=col))

    def rows_to_tuples(self,
                       row_first: int,
                       row_last: int,
                       col_first: int,
                       col_last: int) -> list[tuple]:
        rows = list()
        for row in range(row_first, row_last+1):
            r = tuple(self._ws.row_values(row=row))
            rows.append(r)
        return rows

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

    @classmethod
    def col_index_to_letter(cls, index: int) -> str:
        """
        ========================================================================
         Convert 1 to A, 2 to B, ... , 27 to AA and etc.
        ========================================================================
        """
        letters = str()
        while index > 0:
            index, remainder = divmod(index - 1, 26)
            letters = chr(65 + remainder) + letters
        return letters

    @classmethod
    def to_a1_range(cls,
                    first_row: int,
                    last_row: int,
                    first_col: int,
                    last_col: int) -> str:
        """
        ========================================================================
         Convert to A1-Notation Range, ex: (A1:Z5).
        ========================================================================
        """
        first_col_letter = Sheet.col_index_to_letter(index=first_col)
        last_col_letter = Sheet.col_index_to_letter(index=last_col)
        return f'{first_col_letter}{first_row}:{last_col_letter}{last_row}'
