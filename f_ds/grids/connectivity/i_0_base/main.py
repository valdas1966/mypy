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

    def cost(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return the Edge Cost between adjacent Cells a and b (override).
        ========================================================================
        """
        raise NotImplementedError

    def heuristic(self, a: HasRowCol, b: HasRowCol) -> int:
        """
        ========================================================================
         Return an admissible lower-bound cost from a to b (override).
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
