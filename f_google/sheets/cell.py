from gspread.cell import Cell as GSCell
from f_abstract.mixins.validatable_public import ValidatablePublic
from f_utils import u_str
from typing import Callable


class Cell(ValidatablePublic):
    """
    ============================================================================
     1. Google-Sheets Cell.
     2. Every change in the Cells' Values stores in list Batch.
     3. The Batch can updates all Cells-Changes at once.
    ============================================================================
    """

    def __init__(self,
                 cell: GSCell,
                 add_to_batch: Callable[[GSCell], None]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cell = cell
        self._add_to_batch = add_to_batch
        ValidatablePublic.__init__(self, is_valid=self.value is not None)

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

    def is_empty(self) -> bool:
        """
        ========================================================================
         Return True if the Cell's Values is Empty.
        ========================================================================
        """
        return u_str.is_empty(self.value)

    def __str__(self) -> str:
        """
        ========================================================================
         Return Cell's Value as Cell STR-REPR.
        ========================================================================
        """
        return self.value
