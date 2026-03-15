from __future__ import annotations
import gspread


class Cell(str):
    """
    ========================================================================
     Proxy for a Google Sheet Cell with write support.
     Extends str for backwards-compatible read access.
    ========================================================================
    """

    def __new__(cls,
                value: str,
                ws: gspread.Worksheet,
                row: int,
                col: int,
                cache_row: list[str]) -> Cell:
        """
        ====================================================================
         Create a new Cell (str) instance.
        ====================================================================
        """
        return str.__new__(cls, value)

    def __init__(self,
                 value: str,
                 ws: gspread.Worksheet,
                 row: int,
                 col: int,
                 cache_row: list[str]) -> None:
        """
        ====================================================================
         Init with worksheet reference and 1-based row/col.
        ====================================================================
        """
        self._ws = ws
        self._row = row
        self._col = col
        self._cache_row = cache_row

    @property
    def value(self) -> str:
        """
        ====================================================================
         Return the Cell value as str.
        ====================================================================
        """
        return str(self)

    @value.setter
    def value(self, val: object) -> None:
        """
        ====================================================================
         Write str(val) to the Google Sheet Cell.
        ====================================================================
        """
        text = str(val)
        self._ws.update_cell(self._row, self._col, text)
        self._cache_row[self._col - 1] = text
