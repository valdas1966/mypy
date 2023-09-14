from __future__ import annotations
from f_heuristic_search.alias.grid import Grid
from f_heuristic_search.alias.cell import Cell


class SPP:
    """
    ============================================================================
     Desc: Represents a Shortest-Path-Problem Type in 2D-Grids.
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
        start.name = 'START'
        goal.name = 'GOAL'
        self._grid = grid
        self._start = start
        self._goal = goal

    def __str__(self) -> str:
        res = f'SPP[{self.grid.name}]: '
        res += f'{self.start} -> {self.goal}'
        return res

    def __repr__(self) -> str:
        return str(self)

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def start(self) -> Cell:
        return self._start

    @property
    def goal(self) -> Cell:
        return self._goal

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_traversable: int = 0
                 ) -> SPP:
        grid = Grid.generate(rows=rows,
                             cols=cols,
                             name=name,
                             pct_non_traversable=pct_non_traversable)
        # Ensure the Grid can accommodate both Start and Goal Cells
        if len(grid) < 2:
            return None
        start, goal = grid.cells_random(size=2)
        return SPP(grid, start, goal)
