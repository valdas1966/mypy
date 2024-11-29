from f_ds.stale import Stale
from f_core.mixins.comparable import Comparable
from typing import TypeVar

Item = TypeVar('Item', bound=Comparable)


class HasStale(Stale[Item]):
    """
    ============================================================================
     Mixin-Class for Data-Structures with Stale object.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._stale: Stale[Item] = Stale()

    @property
    def stale(self) -> Stale:
        """
        ========================================================================
         Return a Stale object of the Data-Structure.
        ========================================================================
        """
        return self._stale
