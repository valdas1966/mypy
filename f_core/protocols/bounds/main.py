from f_ds.geometry.bounds import Bounds
from typing import Protocol, TypeVar, runtime_checkable

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
