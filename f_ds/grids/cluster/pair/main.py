from f_core.mixins import Hashable
from f_ds.grids.cluster import ClusterGrid
from typing import Generic, TypeVar

Cluster = TypeVar('Cluster', bound=ClusterGrid)


class PairCluster(Hashable, Generic[Cluster]):
    """
    ============================================================================
     Ordered pair of two clusters, treated as a single hashable component.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 cluster_a: Cluster,
                 cluster_b: Cluster) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cluster_a: Cluster = cluster_a
        self._cluster_b: Cluster = cluster_b

    @property
    def cluster_a(self) -> Cluster:
        """
        ========================================================================
         Return the first cluster.
        ========================================================================
        """
        return self._cluster_a

    @property
    def cluster_b(self) -> Cluster:
        """
        ========================================================================
         Return the second cluster.
        ========================================================================
        """
        return self._cluster_b

    @property
    def key(self) -> tuple[Cluster, Cluster]:
        """
        ========================================================================
         Identity = (cluster_a, cluster_b).
        ========================================================================
        """
        return self._cluster_a, self._cluster_b

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR: 'PairCluster(a, b)'.
        ========================================================================
        """
        return (f'{type(self).__name__}('
                f'{self._cluster_a}, {self._cluster_b})')

    def __repr__(self) -> str:
        """
        ========================================================================
         Return REPR: '<PairCluster: a | b>'.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'{self._cluster_a!r} | {self._cluster_b!r}>')
