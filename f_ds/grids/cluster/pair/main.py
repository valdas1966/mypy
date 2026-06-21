from typing import TypeVar

from f_ds.pair.main import Pair
from f_ds.grids.cluster.i_0_base.main import ClusterGrid


T = TypeVar('T', bound=ClusterGrid)


class PairCluster(Pair[T]):
    """
    ============================================================================
     Ordered Pair of grid Clusters (A, B) with the Manhattan distance
     between their centers. Inherits `a`/`b`/`key`/eq/hash from `Pair`
     (ordered: identity is (A, B)); adds the cluster-specific `distance`.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Cluster A
                 a: T,
                 # Cluster B
                 b: T) -> None:
        """
        ========================================================================
         Init as an ordered Pair of Clusters.
        ========================================================================
        """
        Pair.__init__(self, a=a, b=b, is_ordered=True)

    @property
    def distance(self) -> int:
        """
        ========================================================================
         Return the Manhattan distance between the centers of A and B.
        ========================================================================
        """
        return self.a.center.distance(other=self.b.center)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'PairCluster(a=..., b=..., distance=d)'.
        ========================================================================
        """
        return (f'{type(self).__name__}('
                f'a={self.a}, '
                f'b={self.b}, '
                f'distance={self.distance})')

    def __repr__(self) -> str:
        """
        ========================================================================
         Return '<PairCluster: map=X, a.center=.., b.center=.., distance=d>'.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'map={self.a.map}, '
                f'a.center={self.a.center.key}, '
                f'b.center={self.b.center.key}, '
                f'distance={self.distance}>')
