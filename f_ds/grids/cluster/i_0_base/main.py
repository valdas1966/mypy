from abc import ABC

from f_ds.mixins.collectionable import Collectionable
from f_core.mixins import HasName
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class ClusterGrid(Collectionable[CellMap], HasName, ABC):
    """
    ============================================================================
     Abstract ClusterGrid: a named set of valid CellMaps on a GridMap.
    ============================================================================
     The root of the cluster hierarchy. A cluster is a named collection of
     cells (the members that belong together) that may expose a single
     `representative` cell (center / medoid / seed). Subclasses define the
     shape (Manhattan ball, rectangle, disk, arbitrary seed-BFS, …) by
     filling `_cells` in their own `__init__` and reading them through
     `to_iterable()` — which drives `len`/`in`/`iter`/`bool` via the
     `Collectionable` mixin. Identity (`name`) comes from `HasName`.

     Holds only the grid's NAME (`map: str`), not the grid object. The grid
     is required at construction time by the subclass `_build()` (BFS,
     neighbor lookup, …) and released as soon as `__init__` returns. This
     keeps clusters light: pickle small, can outlive the in-memory grid,
     and don't pin large grids in caller scopes that have already moved on.

     Concrete subclass: `ClusterDiamond` (`../i_1_diamond/`).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap (used at build-time only; not stored)
                 grid: GridMap) -> None:
        """
        ========================================================================
         Snapshot the grid's name into `_map`, set `name` to the concrete
         class name, and initialise an empty cell list. Concrete subclasses
         must consume the `grid` argument inside their own `__init__`
         (typically passed to `_build(grid=...)`) and assign the result to
         `self._cells`; `ClusterGrid` does not retain the grid.
        ========================================================================
        """
        HasName.__init__(self, name=type(self).__name__)
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

    @property
    def members(self) -> list[CellMap]:
        """
        ========================================================================
         Return the Cluster's members as a list (a copy of to_iterable()).
        ========================================================================
        """
        return list(self.to_iterable())

    @property
    def representative(self) -> CellMap | None:
        """
        ========================================================================
         Return the Cluster's representative (center / medoid / seed).
         Default None — subclasses with a distinguished cell override.
        ========================================================================
        """
        return None

    def to_iterable(self) -> list[CellMap]:
        """
        ========================================================================
         Return the underlying cell list. Drives `len()`, `in`, `iter()`,
         `bool()` via the Collectionable mixin.
        ========================================================================
        """
        return self._cells

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'name(size=n)', plus 'rep=…' when the Cluster
         has a representative.
        ========================================================================
        """
        rep = self.representative
        if rep is None:
            return f'{self.name}(size={len(self)})'
        return f'{self.name}(size={len(self)}, rep={rep})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the Cluster.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'map={self.map}, '
                f'cells={len(self)}>')
