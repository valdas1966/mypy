from typing import Protocol, Generic, TypeVar, NamedTuple

T = TypeVar('T', bound=float)


class Bounds(NamedTuple):
    """
    ========================================================================
     A named tuple representing the bounds of an object.
    ========================================================================
     Attributes:
        top: The top coordinate of the bounds.
        left: The left coordinate of the bounds.
        bottom: The bottom coordinate of the bounds.
        right: The right coordinate of the bounds.
    ========================================================================
    """
    top: T
    left: T
    bottom: T
    right: T

class SupportsBounds(Protocol, Generic[T]):
    """
    ========================================================================
     Protocol for objects that have bounds.
    ========================================================================
    """

    def bounds(self) -> Bounds[T]:
        """
        ========================================================================
         Return the bounds of the object as a Bounds object.
        ========================================================================
        """
        ...