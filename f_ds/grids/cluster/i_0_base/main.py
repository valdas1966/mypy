from abc import ABC
from f_ds.mixins.collectionable.main import Collectionable
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class Cluster(Collectionable[CellMap], ABC):
    """
    ============================================================================
     Abstract Cluster: a set of valid CellMaps on a GridMap.

     Holds only the grid's NAME (`map: str`), not the grid object — the
     grid is required at construction time by `_build()` (BFS, etc.) and
     released as soon as `__init__` returns. This keeps clusters light
     (good for pickling and outliving the in-memory grid).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap (used at build-time only; not stored)
                 grid: GridMap) -> None:
        """
        ========================================================================
         Snapshot the grid's name into `_map` and initialise an empty
         cell list. Concrete subclasses must consume the `grid` argument
         inside their own `__init__` (typically passed to
         `_build(grid=...)`) and assign the result to `self._cells`;
         `Cluster` does not retain the grid.
        ========================================================================
        """
        self._map: str = grid.name
        self._cells: list[CellMap] = []

    @property
    def map(self) -> str:
        """
        ========================================================================
         Return the parent grid's NAME (the only grid identity retained).
        ========================================================================
        """
        return self._map

    @property
    def cells(self) -> list[CellMap]:
        """
        ========================================================================
         Return the list of Cells in the Cluster.
        ========================================================================
        """
        return list(self._cells)

    def to_iterable(self) -> list[CellMap]:
        """
        ========================================================================
         Return the underlying cell list. Drives `len()`, `in`, `iter()`,
         `bool()` via the Collectionable mixin.
        ========================================================================
        """
        return self._cells

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the Cluster.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'map={self._map}, '
                f'cells={len(self)}>')
