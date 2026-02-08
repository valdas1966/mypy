from f_core.protocols.comparison import SupportsComparison
from f_core.mixins.equatable.main import Equatable
from functools import total_ordering
from abc import abstractmethod


@total_ordering
class Comparable(Equatable, SupportsComparison):
    """
    ============================================================================
     1. Mixin class for objects that support comparison operations.
     2. @total_ordering decorator automatically generates the additional
       comparison methods to __lt__().
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    @abstractmethod
    def key_comparison(self) -> SupportsComparison:
        """
        ========================================================================
         Return the key for comparison between two Comparable objects.
        ========================================================================
        """
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the current object is less than another object.
        ========================================================================
        """
        if not isinstance(other, Comparable):
            return NotImplemented
        return self.key_comparison() < other.key_comparison()
