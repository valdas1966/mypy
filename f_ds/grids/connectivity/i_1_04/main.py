from f_ds.grids.connectivity.i_0_base.main import ConnectivityBase
from f_ds.geometry.point2d import Point2D


class Connectivity_4(ConnectivityBase):
    """
    ============================================================================
     4-Connectivity (von Neumann): the 4 cardinal neighbors.
    ============================================================================
    """

    # Neighbor Offsets (Clock-Wise: North, East, South, West)
    _OFFSETS = ((-1, 0), (0, 1), (1, 0), (0, -1))

    @property
    def offsets(self) -> tuple[tuple[int, int], ...]:
        """
        ========================================================================
         Return the 4 cardinal (d_row, d_col) offsets (N, E, S, W).
        ========================================================================
        """
        return self._OFFSETS

    def cost(self, a: Point2D, b: Point2D) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells (always 1).
        ========================================================================
        """
        return 1

    def distance(self, a: Point2D, b: Point2D) -> int:
        """
        ========================================================================
         Return the Manhattan (L1) distance from a to b: the minimum
         4-conn path cost, exact on an obstacle-free grid (an
         admissible, consistent heuristic). Owned here, not borrowed —
         the policy is the single source of its movement metric.
        ========================================================================
        """
        d_row = abs(a.row - b.row)
        d_col = abs(a.col - b.col)
        return d_row + d_col
