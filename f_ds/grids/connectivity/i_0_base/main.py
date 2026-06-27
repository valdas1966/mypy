from f_core.mixins.has.row_col import HasRowCol
from typing import Callable


class ConnectivityBase:
    """
    ============================================================================
     Connectivity Policy for a 2D-Grid.
    ============================================================================
    """

    @property
    def offsets(self) -> tuple[tuple[int, int], ...]:
        """
        ========================================================================
         Return the neighbor (d_row, d_col) offsets (override).
        ========================================================================
        """
        raise NotImplementedError

    @property
    def unit(self) -> int:
        """
        ========================================================================
         Scale Factor: true distance = cost / unit (default 1).
        ========================================================================
        """
        return 1

    def is_cardinal(self, a: HasRowCol, b: HasRowCol) -> bool:
        """
        ========================================================================
         Return True if the move a -> b is cardinal (axis-aligned: one
         of N/E/S/W), False if diagonal. Assumes a, b are adjacent.
        ========================================================================
        """
        d_row = a.row - b.row
        d_col = a.col - b.col
        return d_row == 0 or d_col == 0

    def cost(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells a and b (override).
        ========================================================================
        """
        raise NotImplementedError

    def distance(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the minimum cost of any a -> b path on the
         obstacle-free grid (override). A lower bound on the real
         path cost: admissible and consistent as a search heuristic.
         NOTE: not HasRowCol.distance (always Manhattan) -- this is
         the movement-model distance and tracks the cost function.
        ========================================================================
        """
        raise NotImplementedError

    def is_legal_move(self,
                      a: HasRowCol,
                      b: HasRowCol,
                      is_free: Callable[[int, int], bool]) -> bool:
        """
        ========================================================================
         Return True if moving a -> b is legal. Default: always legal
         (cardinal moves never cut a corner). `is_free(row, col)` tells
         whether a cell is passable (for diagonal corner-cut checks).
        ========================================================================
        """
        return True
