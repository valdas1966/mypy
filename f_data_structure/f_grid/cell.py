from __future__ import annotations
from f_abstract.mixins.validatable import Validatable
from f_data_structure.mixins.has_row_col import HasRowCol
from f_const.u_enum import DistanceMetric


class Cell(HasRowCol, Validatable):
    """
    ============================================================================
     Represents a Cell in a 2D-Grid.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: Cell) -> int
           - Returns distance between this Cell and another Cell.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> '(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. comparison funcs based on row-major system.
    ============================================================================
    """

    _row: int                  # Row-Position in the Grid.
    _col: int                  # Col-Position in the Grid
    _is_valid: bool            # Is Traversable in the Grid

    def __init__(self,
                 row: int,
                 col: int = None,
                 is_valid: bool = True
                 ) -> None:
        HasRowCol.__init__(self, row, col)
        Validatable.__init__(self, is_valid)

    def distance(self,
                 other: Cell,
                 metric: DistanceMetric = DistanceMetric.MANHATTAN
                 ) -> int:
        """
        ========================================================================
         Returns the distance between this Cell and another Cell.
        ========================================================================
        """
        if metric == DistanceMetric.MANHATTAN:
            diff_row = abs(self.row - other.row)
            diff_col = abs(self.col - other.col)
            return diff_row + diff_col
