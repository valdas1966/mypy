from f_heuristic_search.alias.grid import Grid
from f_heuristic_search.alias.cell import Cell


class SPP:
    """
    ============================================================================
     Desc: Represents a Shortest-Path-Problem Type.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. grid (Grid)        : Problem Space.
        2. start (Cell)       : Problem's Start-Cell.
        3. goal (Cell)        : Problem's Goal-Cell.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 start: Cell,
                 goal: Cell) -> None:
        self._grid = grid
        self._start = start
        self._goal = goal

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def start(self) -> Cell:
        return self._start

    @property
    def goal(self) -> Cell:
        return self._goal
