from f_ds.grids.connectivity.i_0_base.main import ConnectivityBase
from f_core.mixins.has.row_col import HasRowCol
from typing import Callable

# Neighbor Offsets (Clock-Wise from North: N, NE, E, SE, S, SW, W, NW)
OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1),
           (1, 0), (1, -1), (0, -1), (-1, -1))

# Scaled-Integer Octile Costs (DIAGONAL / CARDINAL ~ sqrt(2))
COST_CARDINAL = 10_000
COST_DIAGONAL = 14_142


class Connectivity8(ConnectivityBase):
    """
    ============================================================================
     8-Connectivity (Moore): 4 cardinals + 4 diagonals, scaled-integer
     octile costs, strict no-corner-cutting (both flanks must be free).
    ============================================================================
    """

    @property
    def offsets(self) -> tuple[tuple[int, int], ...]:
        """
        ========================================================================
         Return the 8 (d_row, d_col) offsets (cardinals + diagonals).
        ========================================================================
        """
        return OFFSETS

    @property
    def unit(self) -> int:
        """
        ========================================================================
         Scale Factor: true distance = cost / unit (= cardinal cost).
        ========================================================================
        """
        return COST_CARDINAL

    def cost(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells: a diagonal move
         costs COST_DIAGONAL, a cardinal move costs COST_CARDINAL.
        ========================================================================
        """
        d_row = abs(a.row - b.row)
        d_col = abs(a.col - b.col)
        is_diagonal = d_row == 1 and d_col == 1
        return COST_DIAGONAL if is_diagonal else COST_CARDINAL

    def heuristic(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the scaled-integer Octile distance from a to b
         (admissible and consistent with the octile cost).
        ========================================================================
        """
        d_row = abs(a.row - b.row)
        d_col = abs(a.col - b.col)
        d_min = min(d_row, d_col)
        d_max = max(d_row, d_col)
        return COST_DIAGONAL * d_min + COST_CARDINAL * (d_max - d_min)

    def is_legal_move(self,
                      a: HasRowCol,
                      b: HasRowCol,
                      is_free: Callable[[int, int], bool]) -> bool:
        """
        ========================================================================
         Return True if moving a -> b is legal. Cardinal moves are
         always legal; a diagonal is legal only when BOTH flank cells
         are free (strict no-corner-cutting). `is_free(row, col)` tells
         whether a cell is passable.
        ========================================================================
        """
        d_row = b.row - a.row
        d_col = b.col - a.col
        is_cardinal = d_row == 0 or d_col == 0
        if is_cardinal:
            return True
        # Flank Cells sharing the clipped corner
        flank_row_free = is_free(a.row, b.col)
        flank_col_free = is_free(b.row, a.col)
        return flank_row_free and flank_col_free
