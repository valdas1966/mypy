from f_ds.nodes.mixins.has_prev import HasPrev
from f_ds.nodes.mixins.has_next import HasNext
from typing import Generic, TypeVar

T = TypeVar('T', bound='HasPrevNext')


class HasPrevNext(Generic[T], HasPrev[T], HasNext[T]):
    """
    ============================================================================
     Mixin for objects that have a previous and next object.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasPrev.__init__(self)
        HasNext.__init__(self)

    def _update_prev(self) -> None:
        """
        ========================================================================
         Update the prev object with self as the next object if it is not None
         and not already set.
        ========================================================================
        """
        if self.prev:
            if self.prev.next is not self:
                self.prev.next = self

    def _update_next(self) -> None:
        """
        ========================================================================
         Update the next object with self as the previous object if it is not
         None and not already set.
        ========================================================================
        """
        if self.next:
            if self.next.prev is not self:
                self.next.prev = self
