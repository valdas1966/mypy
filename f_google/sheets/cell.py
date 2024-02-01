from typing import Callable
from gspread.cell import Cell as GSCell


class Cell:
    """
    ============================================================================
     Google-Sheets Cell.
    ============================================================================
    """

    def __init__(self,
                 cell: GSCell,
                 add_to_batch: Callable[[GSCell], None]) -> None:
        self._cell = cell
        self._add_to_batch = add_to_batch

    @property
    def row(self) -> int:
        return self._cell.row

    @property
    def col(self) -> int:
        return self._cell.col

    @property
    def value(self) -> str:
        return self._cell.value

    @value.setter
    def value(self, val: str) -> None:
        self._cell.value = val
        self._add_to_batch(cell=self._cell)
