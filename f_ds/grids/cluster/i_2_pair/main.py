from f_core.mixins import Tupleable
from f_ds.grids.cluster import ClusterDiamond


class PairCluster(Tupleable):
    """
    ============================================================================
     Ordered pair of two ClusterDiamonds, treated as a single value-record.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 cluster_a: ClusterDiamond,
                 cluster_b: ClusterDiamond) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cluster_a: ClusterDiamond = cluster_a
        self._cluster_b: ClusterDiamond = cluster_b

    @property
    def cluster_a(self) -> ClusterDiamond:
        """
        ========================================================================
         Return the first cluster.
        ========================================================================
        """
        return self._cluster_a

    @property
    def cluster_b(self) -> ClusterDiamond:
        """
        ========================================================================
         Return the second cluster.
        ========================================================================
        """
        return self._cluster_b

    def to_tuple(self) -> tuple[ClusterDiamond, ClusterDiamond]:
        """
        ========================================================================
         Data-tuple = (cluster_a, cluster_b). Drives ==, hash, iter, [], len
         (and ordering) via the Tupleable mixin.
        ========================================================================
        """
        return self._cluster_a, self._cluster_b

    def distance(self) -> int:
        """
        ========================================================================
         Return the Manhattan distance between the two diamonds' centers.
        ========================================================================
        """
        center_a = self._cluster_a.center
        center_b = self._cluster_b.center
        return center_a.distance(center_b)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'PairCluster(a, b)'.
        ========================================================================
        """
        return (f'{type(self).__name__}('
                f'{self._cluster_a}, {self._cluster_b})')
