from f_ds.grids.connectivity.i_0_base.main import ConnectivityBase
from f_core.mixins.has.row_col import HasRowCol


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

    def cost(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells (always 1).
        ========================================================================
        """
        return 1

    def heuristic(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the Manhattan distance from a to b (admissible and
         exact on an obstacle-free grid).
        ========================================================================
        """
        return a.distance(other=b)
