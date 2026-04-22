from typing import Generic, TypeVar
from f_ds.grids.cluster.i_0_base.main import Cluster


T = TypeVar('T', bound=Cluster)


class PairCluster(Generic[T]):
    """
    ============================================================================
     Pair of Clusters (A, B) on a GridMap with Manhattan distance between
     their centers.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Cluster A
                 a: T,
                 # Cluster B
                 b: T,
                 # Pair's Name
                 name: str = 'PairCluster') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._a = a
        self._b = b
        self._name = name

    @property
    def a(self) -> T:
        """
        ========================================================================
         Return Cluster A.
        ========================================================================
        """
        return self._a

    @property
    def b(self) -> T:
        """
        ========================================================================
         Return Cluster B.
        ========================================================================
        """
        return self._b

    @property
    def name(self) -> str:
        """
        ========================================================================
         Return the Pair's Name.
        ========================================================================
        """
        return self._name

    @property
    def distance(self) -> int:
        """
        ========================================================================
         Return the Manhattan distance between the centers of A and B.
        ========================================================================
        """
        return self._a.center.distance(other=self._b.center)

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a flat dict of analytic metadata for this pair, suitable for
         CSV export, structured logging, or downstream dataframes.

         Naming follows the convention:
           (a) Grid-level fields first (domain, map, rows, cols, n_cells_grid).
           (b) Per-pair geometry (center_[ab]_row, center_[ab]_col).
           (c) Shape parameters (steps_a, steps_b).
           (d) Cluster sizes (n_cells_a, n_cells_b).
           (e) Pair summary (distance).

         Assumes each cluster has a '.steps' attribute (satisfied by
         ClusterDiamond). If a future Cluster subclass lacks 'steps', it
         should override this method or provide the attribute.
        ========================================================================
        """
        grid = self._a.grid
        return dict(
            domain=grid.domain,
            map=grid.name,
            rows=grid.rows,
            cols=grid.cols,
            n_cells_grid=len(grid),
            center_a_row=self._a.center.row,
            center_a_col=self._a.center.col,
            center_b_row=self._b.center.row,
            center_b_col=self._b.center.col,
            steps_a=self._a.steps,
            steps_b=self._b.steps,
            n_cells_a=len(self._a),
            n_cells_b=len(self._b),
            distance=self.distance,
        )

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'PairCluster(a=..., b=..., distance=d)'
        ========================================================================
        """
        return (f'{self._name}('
                f'a={self._a}, '
                f'b={self._b}, '
                f'distance={self.distance})')

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the PairCluster --- concise identifier
         with the shared grid, both centers, and the pair distance.
         Full metadata: see to_analytics().
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'grid={self._a.grid.name}, '
                f'a.center={self._a.center.key}, '
                f'b.center={self._b.center.key}, '
                f'distance={self.distance}>')
