from abc import ABC
from f_core.mixins import HasName
from f_ds.mixins.collectionable import Collectionable
from f_ds.grids import GridMap as Grid, CellMap as Cell


class ClusterGrid(Collectionable[Cell], HasName, ABC):
    """
    ============================================================================
     Abstract ClusterGrid: a named set of valid Cell on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap (used at build-time only; not stored)
                 grid: Grid,
                 name: str = 'ClusterGrid') -> None:
        """
        ========================================================================
         Snapshot the grid's name into `_map`, set `name` to the concrete
         class name, and initialise an empty cell list. Concrete subclasses
         must consume the `grid` argument inside their own `__init__`
         (typically passed to `_build(grid=...)`) and assign the result to
         `self._cells`; `ClusterGrid` does not retain the grid.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._map: str = grid.name
        self._cells: list[Cell] = []

    @property
    def map(self) -> str:
        """
        ========================================================================
         Return the parent grid's NAME (the only grid identity retained).
        ========================================================================
        """
        return self._map

    @property
    def cells(self) -> list[Cell]:
        """
        ========================================================================
         Return the list of Cells in the Cluster.
        ========================================================================
        """
        return list(self._cells)

    def to_iterable(self) -> list[Cell]:
        """
        ========================================================================
         Return the underlying cell list.
        ========================================================================
        """
        return self._cells
