from f_ds.grids.cluster.i_0_base.main import Cluster
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class ClusterDiamond(Cluster):
    """
    ============================================================================
     Diamond-shaped (Manhattan-ball) Cluster on a GridMap.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap
                 grid: GridMap,
                 # Center cell of the diamond
                 center: CellMap,
                 # Manhattan radius (steps from center)
                 steps: int,
                 # Cluster's Name
                 name: str = 'ClusterDiamond') -> None:
        """
        ========================================================================
         Init private Attributes and build the diamond via BFS.
        ========================================================================
        """
        Cluster.__init__(self, grid=grid, name=name)
        self._center = center
        self._steps = steps
        self._cells: list[CellMap] = self._build()

    def _build(self) -> list[CellMap]:
        """
        ========================================================================
         BFS from center up to depth <= steps.
         Skips wall (invalid) cells automatically via grid.neighbors.
        ========================================================================
        """
        # An invalid center yields an empty cluster
        if not self._center:
            return []
        # Aliases
        grid = self._grid
        steps = self._steps
        # BFS
        visited: set[tuple[int, int]] = {self._center.key}
        frontier: list[CellMap] = [self._center]
        cells: list[CellMap] = [self._center]
        for _ in range(steps):
            next_frontier: list[CellMap] = []
            for cell in frontier:
                for nbr in grid.neighbors(cell=cell):
                    if nbr.key in visited:
                        continue
                    visited.add(nbr.key)
                    cells.append(nbr)
                    next_frontier.append(nbr)
            frontier = next_frontier
        return cells

    def to_iterable(self) -> list[CellMap]:
        """
        ========================================================================
         Return the valid Cells inside the Diamond.
        ========================================================================
        """
        return self._cells

    @property
    def center(self) -> CellMap:
        """
        ========================================================================
         Return the Center cell of the Diamond.
        ========================================================================
        """
        return self._center

    @property
    def steps(self) -> int:
        """
        ========================================================================
         Return the Manhattan radius (steps from center).
        ========================================================================
        """
        return self._steps

    @property
    def key(self) -> tuple[tuple[int, int], int]:
        """
        ========================================================================
         Return (center.key, steps) for comparison / dedup.
        ========================================================================
        """
        return (self._center.key, self._steps)

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Extend the base Cluster.to_analytics() with diamond-specific fields.
         Adds: steps.
        ========================================================================
        """
        base = super().to_analytics()
        base['steps'] = self._steps
        return base

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR:
         'ClusterDiamond(center=(r,c), steps=s, cells=n)'
        ========================================================================
        """
        return (f'{self._name}('
                f'center={self._center.key}, '
                f'steps={self._steps}, '
                f'cells={len(self)})')

    def __repr__(self) -> str:
        """
        ========================================================================
         Return a debugger-friendly representation including the grid
         context: '<ClusterDiamond: grid=X, center=(r,c), steps=s, cells=n>'
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'grid={self._grid.name}, '
                f'center={self._center.key}, '
                f'steps={self._steps}, '
                f'cells={len(self)}>')
