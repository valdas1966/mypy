from f_core.mixins.hashable.main import Hashable
from f_ds.grids.cluster.i_0_base.main import Cluster
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class ClusterDiamond(Cluster, Hashable):
    """
    ============================================================================
     Diamond-shaped (Manhattan-ball) Cluster on a GridMap.

     Identity (`key`, `__eq__`, `__hash__` via Hashable):
       (map_name, center.key, steps).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap (used at build-time only; not stored)
                 grid: GridMap,
                 # Center cell of the diamond
                 center: CellMap,
                 # Manhattan radius (steps from center)
                 steps: int) -> None:
        """
        ========================================================================
         Init private Attributes and build the diamond via BFS. The grid
         is consumed by `_build` and not retained on `self`.
        ========================================================================
        """
        Cluster.__init__(self, grid=grid)
        self._center: CellMap = center
        self._steps: int = steps
        self._cells = self._build(grid=grid)

    def _build(self, grid: GridMap) -> list[CellMap]:
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
    def key(self) -> tuple[str, tuple[int, int], int]:
        """
        ========================================================================
         Identity: (map_name, center.key, steps). Drives __eq__ / __hash__
         via the Hashable mixin.
        ========================================================================
        """
        return (self._map, self._center.key, self._steps)

    def __repr__(self) -> str:
        """
        ========================================================================
         Return a debugger-friendly representation:
         '<ClusterDiamond: map=X, center=(r,c), steps=s, cells=n>'.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'map={self._map}, '
                f'center={self._center.key}, '
                f'steps={self._steps}, '
                f'cells={len(self)}>')
