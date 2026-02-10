from typing import Protocol, Generic, TypeVar

T = TypeVar('T', int, float)


class SupportsBounds(Protocol, Generic[T]):
    """
    ========================================================================
     Protocol for objects that have bounds.
    ========================================================================
    """

    def bounds(self) -> tuple[T, T, T, T]: ...
    """
    ========================================================================
     Return the bounds of the object as a tuple (top, left, bottom, right).
    ========================================================================
    """
