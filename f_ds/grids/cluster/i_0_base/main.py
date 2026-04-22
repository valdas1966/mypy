from abc import ABC, abstractmethod
from f_ds.mixins.collectionable.main import Collectionable
from f_ds.grids.cell.i_1_map.main import CellMap
from f_ds.grids.grid.map.main import GridMap


class Cluster(Collectionable[CellMap], ABC):
    """
    ============================================================================
     Abstract Cluster: a set of valid CellMaps on a GridMap.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Parent GridMap
                 grid: GridMap,
                 # Cluster's Name
                 name: str = 'Cluster') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid
        self._name = name

    @property
    def grid(self) -> GridMap:
        """
        ========================================================================
         Return the parent GridMap of the Cluster.
        ========================================================================
        """
        return self._grid

    @property
    def name(self) -> str:
        """
        ========================================================================
         Return the Cluster's Name.
        ========================================================================
        """
        return self._name

    @property
    def cells(self) -> list[CellMap]:
        """
        ========================================================================
         Return the list of Cells in the Cluster.
        ========================================================================
        """
        return list(self.to_iterable())

    @property
    @abstractmethod
    def center(self) -> CellMap:
        """
        ========================================================================
         Return the representative center cell of the Cluster.
         Every concrete Cluster must expose a center, used for pair-level
         geometry (e.g. PairCluster.distance).
        ========================================================================
        """
        pass

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a flat dict of analytic metadata for this cluster, suitable
         for CSV export and downstream analysis.

         Base fields:
           (a) Grid-level   -- domain, map, rows, cols, n_cells_grid.
           (b) Cluster core -- center_row, center_col, cells.

         Subclasses should extend via super().to_analytics() and add
         shape-specific keys (e.g. ClusterDiamond adds 'steps').
        ========================================================================
        """
        grid = self._grid
        return dict(
            domain=grid.domain,
            map=grid.name,
            rows=grid.rows,
            cols=grid.cols,
            n_cells_grid=len(grid),
            center_row=self.center.row,
            center_col=self.center.col,
            cells=len(self),
        )

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the Cluster.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'name={self._name}, '
                f'cells={len(self)}>')
