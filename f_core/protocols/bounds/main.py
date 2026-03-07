from __future__ import annotations
from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

if TYPE_CHECKING:
    from f_ds.geometry.bounds import Bounds

T = TypeVar('T', int, float)


@runtime_checkable
class SupportsBounds(Protocol[T]):
    """
    ========================================================================
     Protocol for objects that have bounds.
    ========================================================================
    """

    @property
    def bounds(self) -> Bounds[T]:
        """
        ========================================================================
         Return the bounds of the object as a Bounds object.
        ========================================================================
        """
        ...
