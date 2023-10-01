from __future__ import annotations
from f_data_structure.nodes.node_1_cell import NodeCell as Node
from f_data_structure.f_grid.grid_cells import GridCells as Grid


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem Type in 2D-Grids.
    ============================================================================
    """

    grid: Grid            # SPP 2D-Grid
    start: Node           # SPP Start-Node
    goal: Node            # SPP Goal-Node

    def __init__(self,
                 grid: Grid,
                 start: Node,
                 goal: Node) -> None:
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
    def start(self) -> Node:
        return self._start

    @property
    def goal(self) -> Node:
        return self._goal

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_valid: int = 0
                 ) -> SPP:
        """
        ========================================================================
         Generates a random SPP based on the given arguments, which include the
          grid size, as well as random locations for the start, goal, and
          invalid nodes.
        ========================================================================
        """
        grid = Grid.generate(rows=rows,
                             cols=cols,
                             name=name,
                             pct_non_valid=pct_non_valid)
        # Ensure the Grid can accommodate both Start and Goal Cells
        if len(grid.cells()) < 2:
            return None
        start, goal = grid.cells_random(size=2)
        return SPP(grid, start, goal)
