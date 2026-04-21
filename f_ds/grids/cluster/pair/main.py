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
         Return the representation of the PairCluster.
        ========================================================================
        """
        return (f'<{type(self).__name__}: '
                f'a={self._a.name}, '
                f'b={self._b.name}, '
                f'distance={self.distance}>')
