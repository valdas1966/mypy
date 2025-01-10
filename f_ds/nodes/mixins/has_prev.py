from typing import Generic, TypeVar

T = TypeVar('T', bound='HasPrev')


class HasPrev(Generic[T]):
    """
    ============================================================================
     Mixin for objects that have a previous object.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._prev: T = None

    @property
    def prev(self) -> T:
        """
        ========================================================================
         Return the previous object.
        ========================================================================
        """
        return self._prev   
    
    @prev.setter
    def prev(self, val: T) -> None:
        """
        ========================================================================
         Set the previous object.
        ========================================================================
        """
        self._prev = val
        self._update_prev()


    def _update_prev(self) -> None:
        """
        ========================================================================
         Make additional updates to the previous object.
        ========================================================================
        """
        pass
