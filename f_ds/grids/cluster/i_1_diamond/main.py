from f_core.mixins import Hashable
from f_ds.grids import GridMap as Grid, CellMap as Cell, ClusterGrid


class ClusterDiamond(ClusterGrid, Hashable):
    """
    ============================================================================
     Diamond-shaped (Manhattan-ball) Cluster on a GridMap.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap (used at build-time only; not stored)
                 grid: Grid,
                 # Center cell of the diamond
                 center: Cell,
                 # Manhattan radius (steps from center)
                 steps: int,
                 name: str = 'ClusterDiamond') -> None:
        """
        ========================================================================
         Init private Attributes and build the diamond via BFS. The grid
         is consumed by `_build` and not retained on `self`.
        ========================================================================
        """
        ClusterGrid.__init__(self, grid=grid, name=name)
        self._center: Cell = center
        self._steps: int = steps
        self._cells = self._build(grid=grid)

    @property
    def center(self) -> Cell:
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
    def key(self) -> tuple[str, tuple[int, int], int]:
        """
        ========================================================================
         Identity: (map_name, center.key, steps). Drives __eq__ / __hash__
         via the Hashable mixin.
        ========================================================================
        """
        return self._map, self._center.key, self._steps

    def _build(self, grid: Grid) -> list[Cell]:
        """
        ========================================================================
         BFS from center up to depth <= steps.
        ========================================================================
        """
        # An invalid center yields an empty cluster
        if not self._center:
            return []
        # Aliases
        steps = self._steps
        # BFS
        visited: set[tuple[int, int]] = {self._center.key}
        frontier: list[Cell] = [self._center]
        cells: list[Cell] = [self._center]
        for _ in range(steps):
            next_frontier: list[Cell] = []
            for cell in frontier:
                for nbr in grid.neighbors(cell=cell):
                    if nbr.key in visited:
                        continue
                    visited.add(nbr.key)
                    cells.append(nbr)
                    next_frontier.append(nbr)
            frontier = next_frontier
        return cells

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'ClusterDiamond(center=(r,c), steps=s, cells=n)'.
        ========================================================================
        """
        return (f'{self.name}('
                f'center={self._center.key}, '
                f'steps={self._steps}, '
                f'cells={len(self)})')
