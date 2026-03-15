from __future__ import annotations
import gspread
from f_ds.range import Range
from f_google.services.sheets.cell.main import Cell


class Sheet:
    """
    ============================================================================
     Google Sheets Worksheet.
    ============================================================================
    """

    def __init__(self, ws: gspread.Worksheet) -> None:
        """
        ====================================================================
         Init with a gspread Worksheet.
        ====================================================================
        """
        self._ws = ws
        self._rows: list[list[str]] | None = None

    @property
    def name(self) -> str:
        """
        ====================================================================
         Return the Worksheet Name.
        ====================================================================
        """
        return self._ws.title

    def last_row(self) -> int:
        """
        ====================================================================
         Return the 1-based index of the last row with a non-empty cell.
         Returns 0 if all rows are empty.
        ====================================================================
        """
        self._load()
        for i in range(len(self._rows) - 1, -1, -1):
            if any(cell for cell in self._rows[i]):
                return i + 1
        return 0

    def last_col(self) -> int:
        """
        ====================================================================
         Return the 1-based index of the last column with a non-empty
         cell. Returns 0 if all cells are empty.
        ====================================================================
        """
        self._load()
        result = 0
        for row in self._rows:
            for c in range(len(row), result, -1):
                if row[c - 1]:
                    result = c
                    break
        return result

    def to_range(self) -> Range:
        """
        ====================================================================
         Return all data as a Range.
        ====================================================================
        """
        self._load()
        return Range(data=self._rows)

    def insert_row(self, row: int) -> None:
        """
        ====================================================================
         Insert an empty row at the given 1-based position.
         Pushes existing rows down.
        ====================================================================
        """
        self._load()
        cols = len(self._rows[0]) if self._rows else 0
        self._ws.insert_row(values=[''] * cols, index=row)
        self._rows.insert(row - 1, [''] * cols)

    def delete_row(self, row: int) -> None:
        """
        ====================================================================
         Delete the row at the given 1-based position.
        ====================================================================
        """
        self._load()
        self._ws.delete_rows(row)
        self._rows.pop(row - 1)

    def _to_cells(self, row_index: int) -> list[Cell]:
        """
        ====================================================================
         Convert a cached row to a list of Cell proxies.
        ====================================================================
        """
        data = self._rows[row_index]
        row_1based = row_index + 1
        return [Cell(value=data[c],
                     ws=self._ws,
                     row=row_1based,
                     col=c + 1,
                     cache_row=data)
                for c in range(len(data))]

    def _load(self) -> None:
        """
        ====================================================================
         Lazy-load all values from the Worksheet.
        ====================================================================
        """
        if self._rows is None:
            self._rows = self._ws.get_all_values()

    def __getitem__(self, key: int | slice) -> list[Cell] | Range:
        """
        ====================================================================
         Return a list of Cells by Index or a Range by Slice.
        ====================================================================
        """
        self._load()
        if isinstance(key, slice):
            return Range(data=self._rows[key])
        return self._to_cells(row_index=key)
