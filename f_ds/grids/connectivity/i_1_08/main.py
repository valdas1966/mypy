from f_ds.grids.connectivity.i_0_base.main import ConnectivityBase
from f_ds.geometry.point2d import Point2D
from typing import Callable


class Connectivity_8(ConnectivityBase):
    """
    ============================================================================
     1. 8-Connectivity (Moore): 4 cardinals + 4 diagonals.
     2. Scaled-integer octile costs.
     3. Strict no-corner-cutting (both flanks must be free).
    ============================================================================
    """

    # Neighbor Offsets (Clock-Wise from North: N, NE, E, SE, S, SW, W, NW)
    _OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1),
                (1, 0), (1, -1), (0, -1), (-1, -1))

    # Scaled-Integer Octile Costs (14142 = round(sqrt(2) * 10000))
    _COST_CARDINAL = 10_000
    _COST_DIAGONAL = 14_142

    @property
    def offsets(self) -> tuple[tuple[int, int], ...]:
        """
        ========================================================================
         Return the 8 (d_row, d_col) offsets (cardinals + diagonals).
        ========================================================================
        """
        return self._OFFSETS

    @property
    def unit(self) -> int:
        """
        ========================================================================
         Scale Factor: true distance = cost / unit (= cardinal cost).
        ========================================================================
        """
        return self._COST_CARDINAL

    def cost(self, a: Point2D, b: Point2D) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells: a diagonal move
         costs _COST_DIAGONAL, a cardinal move costs _COST_CARDINAL.
        ========================================================================
        """
        is_cardinal = self.is_cardinal(a=a, b=b)
        return self._COST_CARDINAL if is_cardinal else self._COST_DIAGONAL

    def distance(self, a: Point2D, b: Point2D) -> int:
        """
        ========================================================================
         Return the scaled-integer Octile distance from a to b: the
         minimum 8-conn path cost, exact on an obstacle-free grid
         (admissible and consistent with the octile edge cost).
         NOTE: this is the octile metric, NOT Manhattan — do not route
         8-conn search through a cell's Manhattan distance, which
         over-estimates here and would be an inadmissible heuristic.
        ========================================================================
        """
        d_row = abs(a.row - b.row)
        d_col = abs(a.col - b.col)
        d_min = min(d_row, d_col)
        d_max = max(d_row, d_col)
        # d_min diagonal steps, then the remaining (d_max - d_min) straight
        diagonal_cost = self._COST_DIAGONAL * d_min
        straight_cost = self._COST_CARDINAL * (d_max - d_min)
        return diagonal_cost + straight_cost

    def is_legal_move(self,
                      a: Point2D,
                      b: Point2D,
                      is_free: Callable[[int, int], bool]) -> bool:
        """
        ========================================================================
         Return True if moving a -> b is legal. Cardinal moves are
         always legal; a diagonal is legal only when BOTH flank cells
         are free (strict no-corner-cutting). `is_free(row, col)` tells
         whether a cell is passable.
        ========================================================================
        """
        if self.is_cardinal(a=a, b=b):
            return True
        # Flank Cells sharing the clipped corner
        flank_row_free = is_free(a.row, b.col)
        flank_col_free = is_free(b.row, a.col)
        return flank_row_free and flank_col_free
