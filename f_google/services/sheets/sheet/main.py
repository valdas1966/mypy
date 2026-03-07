from __future__ import annotations
import gspread
from f_ds.range import Range


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

    def _load(self) -> None:
        """
        ====================================================================
         Lazy-load all values from the Worksheet.
        ====================================================================
        """
        if self._rows is None:
            self._rows = self._ws.get_all_values()

    def last_row(self) -> int:
        """
        ====================================================================
         Return the index of the last row with a non-empty cell.
         Returns -1 if all rows are empty.
        ====================================================================
        """
        self._load()
        for i in range(len(self._rows) - 1, -1, -1):
            if any(cell for cell in self._rows[i]):
                return i
        return -1

    def last_col(self) -> int:
        """
        ====================================================================
         Return the index of the last column with a non-empty cell.
         Returns -1 if all cells are empty.
        ====================================================================
        """
        self._load()
        result = -1
        for row in self._rows:
            for c in range(len(row) - 1, result, -1):
                if row[c]:
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

    def __getitem__(self, key: int | slice) -> list[str] | Range:
        """
        ====================================================================
         Return a Row by Index or a Range by Slice.
        ====================================================================
        """
        self._load()
        if isinstance(key, slice):
            return Range(data=self._rows[key])
        return self._rows[key]
