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

    __ROW_MAX = 10000000
    __VALUE_EMPTY = str()

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

    def row_last(self, col: int, row_first: int = 1) -> int:
        """
        ========================================================================
         Return the Last non-empty Row in the given Col.
        ========================================================================
        """
        row = row_first + 1
        while row < Sheet.__ROW_MAX:
            if self._ws.cell(row, col) == Sheet.__VALUE_EMPTY:
                return row - 1
            row += 1
        return None

    def to_tuples(self,
                  col_first: int,
                  col_last: int,
                  row_first: int,
                  row_last: int = None) -> list[tuple]:
        if not row_last:
            row_last = self.row_last(col=col_first, row_first=row_first)
        a1_range = Sheet.to_a1_range(row_first=row_first,
                                     row_last=row_last,
                                     col_first=col_first,
                                     col_last=col_last)
        range = self._ws.range(a1_range)

        def to_tuples(self, col_first: int, col_last: int, row_first: int,
                      row_last: int = None) -> list[tuple]:
            if row_last is None:
                row_last = self.row_last(col=col_first, row_first=row_first)
                if row_last is None:
                    return []  # Return an empty list if no last row is found

            a1_range = self.to_a1_range(row_first=row_first, row_last=row_last,
                                        col_first=col_first, col_last=col_last)
            cells = self._ws.range(a1_range)

            num_columns = col_last - col_first + 1
            return [tuple(cell.value for cell in cells[i:i + num_columns]) for i
                    in range(0, len(cells), num_columns)]

    def update(self) -> None:
        """
        ========================================================================
         Update the Google-Sheet with the updates in the Batch.
        ========================================================================
        """
        self._batch.run()

    def __getitem__(self, coords: tuple[int, int]) -> Cell:
        """
        ========================================================================
         Return a Cell by given Coordinates.
        ========================================================================
        """
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
                    row_first: int,
                    row_last: int,
                    col_first: int,
                    col_last: int) -> str:
        """
        ========================================================================
         Convert to A1-Notation Range, ex: (A1:Z5).
        ========================================================================
        """
        letter_col_first = Sheet.col_index_to_letter(index=col_first)
        letter_col_last = Sheet.col_index_to_letter(index=col_last)
        return f'{letter_col_first}{row_first}:{letter_col_last}{row_last}'
