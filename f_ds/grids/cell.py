from __future__ import annotations
from typing import Sequence, Iterable
from f_core.mixins.validatable_public import ValidatablePublic
from f_core.mixins.has_row_col import HasRowCol


class Cell(HasRowCol, ValidatablePublic):
    """
    ============================================================================
     Cell in the 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 row: int = None,
                 col: int = None,
                 is_valid: bool = True
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRowCol.__init__(self, row, col)
        ValidatablePublic.__init__(self, is_valid)

    def distance(self, other: Cell) -> int:
        """
        ========================================================================
         Return the distance between the two Cells.
        ========================================================================
        """
        diff_row = abs(self.row - other.row)
        diff_col = abs(self.col - other.col)
        return diff_row + diff_col
    
    def farthest(self, cells: Iterable[Cell]) -> Cell:
        """
        ========================================================================
         Return the farthest Cell from the current Cell.
        ========================================================================
        """
        # Init max values with not-logical values
        # (so that the first candidate will be good)
        dist_max = 0
        cell_max = None
        # Iterate over the candidates to find the farthest one
        for cell in cells:
            # Get the distance between the current cell and the candidate
            dist = self.distance(cell)
            # Update the max distance and candidate if the current distance
            #  is greater than the current max distance.
            if dist > dist_max:
                dist_max = dist
                cell_max = cell
        # Return the farthest cell
        return cell_max

    @staticmethod
    def invalidate(cells: Sequence[Cell]) -> None:
        """
        ========================================================================
         Invalidate multiple cells.
        ========================================================================
        """
        for cell in cells:
            cell.set_invalid()
            