from f_core.protocols.comparison import SupportsComparison
from f_core.mixins.equatable.main import Equatable
from abc import abstractmethod


class Comparable(Equatable, SupportsComparison):
    """
    ============================================================================
     Mixin class for objects that support comparison operations.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    @property
    @abstractmethod
    def key(self) -> SupportsComparison:
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
        return self.key < other.key

    def __le__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the current object is less than or equal to another.
        ========================================================================
        """
        return self.key <= other.key

    def __gt__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the current object is greater than another object.
        ========================================================================
        """
        return self.key > other.key

    def __ge__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the current object is greater than or equal to another.
        ========================================================================
        """
        return self.key >= other.key
